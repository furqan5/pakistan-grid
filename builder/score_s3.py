"""Gate check S3: match the 69 NGC stations of PER FY2024-25 Figure 1 to buses of a topology build.

The rule is fixed in gate/PREREGISTRATION.md ("S3 match rule") and the aliases in gate/s3_aliases.csv.
  python builder/score_s3.py --selftest          # each station must match its own PER/PSS spellings (no OSM data)
  python builder/score_s3.py [build_dir]         # default osm/build/explicit; writes s3_matches.csv + s3_report.md
"""
import csv
import json
import pathlib
import re
import sys
import unicodedata

import networkx as nx

ROOT = pathlib.Path(__file__).resolve().parents[1]
ALIASES = ROOT / "gate" / "s3_aliases.csv"
PLANT_OK = {"TPS M.garh", "S.Y. Guddu", "NGPS"}  # PER entries that are plant switchyards; only these may match plant buses
ROMAN = {"ii": "2", "iii": "3", "iv": "4"}
VOWELS = set("aeiou")


def norm_word(w):
    out = []
    for ch in w:
        if ch == "h" and out and out[-1].isalpha() and out[-1] not in VOWELS:
            continue  # drop an h that follows a consonant: kh->k, gh->g, sh->s
        if out and ch == out[-1] and ch.isalpha():
            continue  # collapse doubled letters
        out.append(ch)
    return "".join(out)


def words(s):
    s = unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode().lower()
    toks = re.sub(r"[^a-z0-9]+", " ", s).split()
    merged, run = [], []
    for t in toks + [None]:  # sentinel flushes the last run
        if t is not None and len(t) == 1 and t.isalpha():
            run.append(t)
            continue
        if len(run) > 1:
            merged.append("".join(run))
        elif len(run) == 1:
            merged.append(("\x00", run[0]))  # lone single letter, resolved below
        run = []
        if t is not None:
            merged.append(t)
    out = []
    for i, t in enumerate(merged):
        if isinstance(t, tuple):
            letter = t[1]
            nxt = merged[i + 1] if i + 1 < len(merged) else None
            if letter == "i":
                out.append("1")
            elif isinstance(nxt, str) and nxt.isalpha() and nxt not in ROMAN:
                merged[i + 1] = letter + nxt  # "M.garh" -> "mgarh", "L/Wala" -> "lwala"
            else:
                out.append(letter)
            continue
        out.append(ROMAN.get(t, t))
    return [norm_word(w) for w in out]


def alias_matches(alias, name):
    aw, nw = words(alias), words(name)
    if not aw or not nw:
        return False
    if set(aw) <= set(nw):
        return True
    a, n = "".join(aw), "".join(nw)
    return len(a) >= 6 and a in n


def lev1(a, b):
    if abs(len(a) - len(b)) > 1 or a == b:
        return a == b
    if len(a) == len(b):
        return sum(x != y for x, y in zip(a, b)) == 1
    if len(a) > len(b):
        a, b = b, a
    return any(a == b[:i] + b[i + 1:] for i in range(len(b)))


def near_miss(alias, name):
    nw = words(name)
    return any(len(w) >= 5 and any(lev1(w, x) for x in nw if len(x) >= 5) for w in words(alias))


def load_aliases():
    rows = list(csv.DictReader(open(ALIASES, encoding="utf-8")))
    for r in rows:
        r["kv"] = int(r["kv"])
        r["alias_list"] = [a.strip() for a in r["aliases"].split("|") if a.strip()]
        r["key"] = f"{r['per_name']}@{r['kv']}"
    return rows


def selftest():
    """Every station must match its own PER name and every quoted PSS name in its source column."""
    rows = load_aliases()
    fails = 0
    for r in rows:
        tests = [r["per_name"]] + re.findall(r"'([^']+)'", r["source"])
        for t in tests:
            hit = [a for a in r["alias_list"] if alias_matches(a, t)]
            if not hit:
                fails += 1
                print(f"FAIL {r['key']}: own spelling {t!r} -> {words(t)}; aliases -> {[words(a) for a in r['alias_list']]}")
    print(f"self-test: {sum(1 + len(re.findall(chr(39) + '([^' + chr(39) + ']+)' + chr(39), r['source'])) for r in rows)} spellings, {fails} failures")
    return fails == 0


def max_matching(rows, cands, edge_fn):
    G = nx.Graph()
    L = [r["key"] for r in rows]
    G.add_nodes_from(L, bipartite=0)
    for r in rows:
        for c in cands:
            if c["kv"] != r["kv"]:
                continue
            if c["kind"] == "P" and r["per_name"] not in PLANT_OK:
                continue
            how = edge_fn(r, c)
            if how:
                G.add_edge(r["key"], "B:" + c["bus"], how=how)
    M = nx.bipartite.maximum_matching(G, top_nodes=L)
    return {k: (M[k][2:], G.edges[k, M[k]]["how"]) for k in L if k in M}


def score(build_dir):
    rows = load_aliases()
    B = list(csv.DictReader(open(build_dir / "buses.csv", encoding="utf-8")))
    S = {r["id"]: r for r in csv.DictReader(open(build_dir / "stations.csv", encoding="utf-8"))}
    P = {r["id"]: r for r in csv.DictReader(open(build_dir / "plants.csv", encoding="utf-8"))}
    cfg = json.loads((ROOT / "builder" / "config.json").read_text(encoding="utf-8"))
    hints = {k: v["name"] for k, v in cfg.get("station_name_hints", {}).items() if not k.startswith("_")}
    cands = []
    for b in B:
        if b["kind"] not in "SP" or b["prov"] not in ("substation", "converter", "plant"):
            continue
        src = S[b["ref"]] if b["kind"] == "S" else P[b["ref"]]
        names = [n.strip() for n in src["all_names"].split(" | ") if n.strip()]
        hint = [hints[m] for m in src.get("members", "").split(";") if m in hints] if b["kind"] == "S" else []
        cands.append({"bus": b["bus"], "kind": b["kind"], "kv": int(b["kv"]), "in_main": b["in_main"] == "1",
                      "names": names, "hint": hint, "lat": b["lat"], "lon": b["lon"]})
    by_bus = {c["bus"]: c for c in cands}

    def by_name(r, c):
        for a in r["alias_list"]:
            for n in c["names"]:
                if alias_matches(a, n):
                    return f"name: alias '{a}' ~ '{n}'"
        return None

    def by_any(r, c):
        h = by_name(r, c)
        if h:
            return h
        for a in r["alias_list"]:
            for n in c["hint"]:
                if alias_matches(a, n):
                    return f"hint: '{n}'"
        for a in r["alias_list"]:
            for n in c["names"]:
                if near_miss(a, n):
                    return f"near-miss: alias '{a}' ~ '{n}'"
        return None

    main = [c for c in cands if c["in_main"]]
    m_scored = max_matching(rows, main, by_name)
    m_anycomp = max_matching(rows, cands, by_name)
    m_all = max_matching(rows, cands, by_any)

    out = []
    for r in rows:
        k = r["key"]
        if k in m_scored:
            tier, (bus, how) = "scored (name, main component)", m_scored[k]
        elif k in m_anycomp:
            tier, (bus, how) = "name, outside main component", m_anycomp[k]
        elif k in m_all:
            tier, (bus, how) = ("hint" if m_all[k][1].startswith("hint") else "near-miss"), m_all[k]
        else:
            tier, bus, how = "unmatched", "", ""
        c = by_bus.get(bus, {})
        used = re.match(r"(?:name|near-miss): alias '([^']+)'", how or "")
        out.append({"per_name": r["per_name"], "kv": r["kv"], "region": r["region"], "tier": tier, "bus": bus,
                    "bus_names": " | ".join(c.get("names", [])), "how": how,
                    # the first alias of each row is the PER spelling; any other alias of a structural row is the [VERIFY] link
                    "structural_alias": int(r["identity"].startswith("structural") and bool(used)
                                            and used.group(1) != r["alias_list"][0]),
                    "lat": c.get("lat", ""), "lon": c.get("lon", "")})
    with open(build_dir / "s3_matches.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(out[0].keys()))
        w.writeheader()
        w.writerows(out)

    n_scored = len(m_scored)
    verdict = "PASS" if n_scored >= 65 else ("FAIL (60-64: decision rule open, see gate)" if n_scored >= 60 else "NO-GO (< 60)")
    struct = sum(o["structural_alias"] for o in out if o["tier"].startswith("scored"))
    L = [f"# S3 — NGC station name match ({build_dir.name} build)\n",
         "Rule: gate/PREREGISTRATION.md, \"S3 match rule\". Aliases: gate/s3_aliases.csv. Doubtful pairs are reported, never removed.\n",
         f"- **Scored S3 (name matches, main component): {n_scored} / 69 → {verdict}** (pass ≥ 65; no-go < 60)",
         f"  - 500 kV: {sum(1 for k in m_scored if k.endswith('@500'))} / 20; 220 kV: {sum(1 for k in m_scored if k.endswith('@220'))} / 49",
         f"  - scored matches that rely on a structural alias: {struct}",
         f"- Name matches anywhere in the build: {len(m_anycomp)} / 69",
         f"- Name + location hints + near-misses (reported only): {len(m_all)} / 69\n",
         "| PER station | kV | tier | bus | OSM names | how | lat, lon |", "|---|---|---|---|---|---|---|"]
    for o in out:
        L.append(f"| {o['per_name']} | {o['kv']} | {o['tier']} | {o['bus'] or '—'} | {o['bus_names'] or '—'} | {o['how'] or '—'} | "
                 f"{o['lat']}, {o['lon']} |" if o["bus"] else f"| {o['per_name']} | {o['kv']} | {o['tier']} | — | — | — | — |")
    (build_dir / "s3_report.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print("\n".join(L[:8]))
    return n_scored


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if "--selftest" in sys.argv:
        sys.exit(0 if selftest() else 1)
    score(pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "osm" / "build" / "explicit")
