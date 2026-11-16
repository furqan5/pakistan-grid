#!/usr/bin/env python
"""Day 2 topology builder: OpenStreetMap power data (Overpass JSON) -> bus/branch tables for Pakistan.

Data (c) OpenStreetMap contributors, ODbL 1.0. Any released derivative must stay ODbL.

Usage:
    python builder/build_topology.py              # with voltage inference  -> osm/build/inferred/
    python builder/build_topology.py --no-infer   # explicit voltage tags only -> osm/build/explicit/

Rules and tolerances live in builder/config.json. Every endpoint decision is written to match_log.csv.
Planar operations use an equirectangular projection at 30 deg N (E-W scale error up to ~8% at the
north/south extremes; used only for snapping tolerances). Lengths use haversine along the OSM geometry.
"""
from __future__ import annotations

import argparse
import collections
import csv
import json
import math
import re
from pathlib import Path

import networkx as nx
import numpy as np
import shapely
from shapely.geometry import LineString, Point, Polygon
from shapely.ops import polygonize, unary_union
from shapely.strtree import STRtree

ROOT = Path(__file__).resolve().parents[1]
CFG = json.loads((ROOT / "builder" / "config.json").read_text(encoding="utf-8"))
RAW = ROOT / "osm" / "raw"
R_EARTH = 6371008.8
COS0 = math.cos(math.radians(30.0))

# PER FY2024-25 Figure 1: the 20 NGC 500 kV grid stations, with name aliases seen in OSM/NTDC usage.
# Day 5: every name-like tag kept per station/plant member, for the S3 name match (gate/PREREGISTRATION.md).
NAME_KEYS = ("name", "name:en", "alt_name", "official_name", "old_name", "short_name")

NGC_500KV = {
    "Rawat": ["rawat", "rewat"], "Peshawar": ["peshawar"], "Gatti": ["gatti"], "Nokhar": ["nokhar"],
    "S.K.P (Sheikhupura)": ["sheikhupura", "skp", "s.k.p"], "New Lahore": ["new lahore", "lahore new"],
    "West FSD": ["faisalabad west", "west fsd", "fsd west", "fbd west", "faisalabad-west", "faisalabad (west)"],
    "Yousafwala": ["yousafwala", "yusufwala", "yousaf wala"], "Multan": ["multan"],
    "M.garh": ["muzaffargarh", "m.garh", "mgarh", "m garh"],
    "D.G. Khan": ["dera ghazi khan", "dg khan", "d.g. khan", "d.g.khan", "d g khan"],
    "RYK": ["rahim yar khan", "ryk", "r.y. khan", "r.y.khan", "rahimyar khan"],
    "TPS M.garh": ["tps muzaffargarh", "muzaffargarh thermal", "tps m.garh", "kot addu"],
    "Dadu": ["dadu"], "Guddu": ["guddu"], "Jamshoro": ["jamshoro"],
    "NKI": ["nki", "new karachi", "karachi interconnect"], "Shikarpur": ["shikarpur"],
    "747 Guddu": ["747", "guddu 747"], "Moro": ["moro"],
}


# ----------------------------------------------------------------------------- helpers
def xy(lon, lat):
    return (R_EARTH * math.radians(lon) * COS0, R_EARTH * math.radians(lat))


def lonlat(x, y):
    return (math.degrees(x / (R_EARTH * COS0)), math.degrees(y / R_EARTH))


def hav_m(lat1, lon1, lat2, lon2):
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp, dl = p2 - p1, math.radians(lon2 - lon1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * R_EARTH * math.asin(min(1.0, math.sqrt(a)))


def parse_kv(v):
    out = []
    if not v:
        return out
    for p in re.split(r"[;,/]", str(v)):
        m = re.search(r"(\d+(?:\.\d+)?)", p)
        if not m:
            continue
        x = float(m.group(1))
        out.append(int(round(x / 1000 if x >= 1000 else x)))
    return out


def parse_int(v):
    if v is None:
        return None
    m = re.search(r"\d+", str(v))
    return int(m.group(0)) if m else None


def name_stem(name):
    if not name:
        return ""
    s = name.lower()
    s = re.sub(r"\d+(\.\d+)?\s*/?\s*\d*\s*k\s*v", " ", s)
    s = re.sub(r"[^a-z0-9 ]", " ", s)
    s = re.sub(r"\b(grid|station|substation|sub|gs|g s|switchyard|switching|kv|power|house|ntdc|ngc|wapda|ltd|limited|the|of|pvt)\b", " ", s)
    return " ".join(s.split())


def element_geom(el):
    t = el["type"]
    if t == "node":
        return Point(xy(el["lon"], el["lat"]))
    if t == "way":
        pts = [xy(p["lon"], p["lat"]) for p in (el.get("geometry") or []) if p]
        if len(pts) >= 4 and el["nodes"][0] == el["nodes"][-1]:
            poly = Polygon(pts)
            if not poly.is_valid:
                poly = poly.buffer(0)
            if not poly.is_empty:
                return poly
        if len(pts) >= 2:
            return LineString(pts).buffer(10)
        return Point(pts[0]) if pts else None
    if t == "relation":
        lines = []
        for m in el.get("members", []):
            g = m.get("geometry")
            if m.get("type") == "way" and g:
                pts = [xy(p["lon"], p["lat"]) for p in g if p]
                if len(pts) >= 2:
                    lines.append(LineString(pts))
        if lines:
            polys = list(polygonize(unary_union(lines)))
            return unary_union(polys) if polys else unary_union(lines).convex_hull
    return None


def exclusion_reason(tags):
    if tags.get("line") in CFG["exclude_line_values"]:
        return f"line={tags.get('line')}"
    for k in CFG["exclude_lifecycle_keys"]:
        if k in tags or tags.get("lifecycle") == k or tags.get("status") == k:
            return f"lifecycle:{k}"
    return None


class DSU:
    def __init__(self, n):
        self.p = list(range(n))

    def find(self, a):
        while self.p[a] != a:
            self.p[a] = self.p[self.p[a]]
            a = self.p[a]
        return a

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            self.p[rb] = ra


def load(name):
    d = json.loads((RAW / f"{name}.json").read_text(encoding="utf-8"))
    if d.get("remark"):
        raise SystemExit(f"{name}.json carries an Overpass remark (likely truncated): {d['remark']}")
    return d


# ----------------------------------------------------------------------------- build
def build(infer: bool):
    out_dir = ROOT / "osm" / "build" / ("inferred" if infer else "explicit")
    out_dir.mkdir(parents=True, exist_ok=True)
    min_kv = CFG["min_voltage_kv"]
    log = []  # match log rows
    stats = collections.Counter()

    subs_json, plants_json, lines_json = load("substations"), load("plants"), load("lines")
    osm_base = lines_json.get("osm3s", {}).get("timestamp_osm_base", "")

    # ---- station features (substations) and plants
    feats = []
    for el in subs_json["elements"]:
        g = element_geom(el)
        if g is None or g.is_empty:
            stats["substation_feature_no_geom"] += 1
            continue
        tags = el.get("tags", {})
        feats.append({
            "osm": f"{el['type'][0]}{el['id']}", "geom": g, "tags": tags,
            "name": tags.get("name:en") or tags.get("name") or "", "kvs": [k for k in parse_kv(tags.get("voltage"))],
            "all_names": [tags[k] for k in NAME_KEYS if tags.get(k)],
            "subtype": tags.get("substation", ""), "operator": tags.get("operator", ""),
        })
    stats["substation_features"] = len(feats)

    dsu = DSU(len(feats))
    geoms = [f["geom"] for f in feats]
    tree = STRtree(geoms)
    a, b = tree.query(geoms, predicate="dwithin", distance=CFG["station_grouping"]["touch_or_near_m"])
    for i, j in zip(a, b):
        if i != j:
            dsu.union(int(i), int(j))
    stems = [name_stem(f["name"]) for f in feats]
    a, b = tree.query(geoms, predicate="dwithin", distance=CFG["station_grouping"]["same_name_stem_m"])
    for i, j in zip(a, b):
        if i != j and stems[i] and stems[i] == stems[j]:
            dsu.union(int(i), int(j))

    groups = collections.defaultdict(list)
    for i in range(len(feats)):
        groups[dsu.find(i)].append(i)
    stations = []
    for sid, members in enumerate(sorted(groups.values(), key=lambda m: min(m))):
        fs = [feats[i] for i in members]
        names = [f["name"] for f in fs if f["name"]]
        # Day 5: tie-break on the name itself; before this, ties followed Python's per-process string hashing.
        name = max(sorted(set(names)), key=lambda n: (names.count(n), len(n), n)) if names else ""
        geom = unary_union([f["geom"] for f in fs])
        c = geom.centroid
        lon, lat = lonlat(c.x, c.y)
        subtypes = sorted({f["subtype"] for f in fs if f["subtype"]})
        prov = "converter" if ("converter" in subtypes or re.search(r"(?i)converter|hvdc", name)) else "substation"
        ops = sorted({f["operator"] for f in fs if f["operator"]})
        stations.append({
            "id": f"S{sid:04d}", "name": name, "members": ";".join(f["osm"] for f in fs), "n_members": len(fs),
            "geom": geom, "lat": lat, "lon": lon, "tag_kvs": sorted({k for f in fs for k in f["kvs"] if k >= min_kv}),
            "subtypes": ";".join(subtypes), "operator": ";".join(ops), "prov": prov,
            "all_names": " | ".join(dict.fromkeys(n for f in fs for n in f["all_names"])),
        })
    stats["stations_after_grouping"] = len(stations)

    plants = []
    for el in plants_json["elements"]:
        g = element_geom(el)
        if g is None or g.is_empty:
            continue
        tags = el.get("tags", {})
        c = g.centroid
        lon, lat = lonlat(c.x, c.y)
        plants.append({
            "id": f"P{len(plants):04d}", "osm": f"{el['type'][0]}{el['id']}", "geom": g, "lat": lat, "lon": lon,
            "name": tags.get("name:en") or tags.get("name") or "", "source": tags.get("plant:source", ""),
            "output": tags.get("plant:output:electricity", ""), "operator": tags.get("operator", ""),
            "tag_kvs": sorted({k for k in parse_kv(tags.get("voltage")) if k >= min_kv}), "prov": "plant",
            "all_names": " | ".join(dict.fromkeys(tags[k] for k in NAME_KEYS if tags.get(k))),
        })
    stats["plants"] = len(plants)

    # ---- lines
    node_ll = {}
    ways = []
    for el in lines_json["elements"]:
        if el["type"] != "way":
            continue
        tags = el.get("tags", {})
        stats["ways_fetched"] += 1
        reason = exclusion_reason(tags)
        kvs_all = parse_kv(tags.get("voltage"))
        kvs = [k for k in kvs_all if k >= min_kv]
        if reason is None and kvs_all and not kvs:
            reason = "below_min_kv"
        geom = el.get("geometry") or []
        if reason is None and (len(geom) < 2 or any(p is None for p in geom)):
            reason = "bad_geometry"
        if reason:
            stats[f"way_excluded:{reason}"] += 1
            continue
        for nid, p in zip(el["nodes"], geom):
            node_ll[nid] = (p["lat"], p["lon"])
        circuits = parse_int(tags.get("circuits"))
        cables = parse_int(tags.get("cables"))
        hvdc = tags.get("frequency") == "0" or any(k >= CFG["hvdc"]["voltage_kv_min"] for k in kvs)
        ways.append({
            "id": el["id"], "nodes": el["nodes"], "tags": tags, "kvs": kvs, "hvdc": hvdc,
            "circuits": circuits if circuits else (max(1, cables // 3) if cables else 1),
            "circuits_src": "circuits" if circuits else ("cables/3" if cables else "default1"),
            "power": tags.get("power"), "name": tags.get("name", ""),
        })
    stats["ways_kept"] = len(ways)

    # ---- which nodes lie inside a station / plant polygon (buffered)
    buf = CFG["endpoint_matching"]["polygon_buffer_m"]
    node_ids = list(node_ll)
    pts = shapely.points([xy(node_ll[n][1], node_ll[n][0]) for n in node_ids])
    node_term = {}

    def assign_inside(targets, kind):
        if not targets:
            return
        bgeoms = [t["geom"].buffer(buf) for t in targets]
        tr = STRtree(bgeoms)
        pi, ti = tr.query(pts, predicate="intersects")
        best = {}
        for p_i, t_i in zip(pi, ti):
            nid = node_ids[int(p_i)]
            if nid in node_term:  # substations take priority over plants
                continue
            d = targets[int(t_i)]["geom"].distance(pts[int(p_i)])
            if nid not in best or d < best[nid][0]:
                best[nid] = (d, targets[int(t_i)]["id"])
        for nid, (_, tid) in best.items():
            node_term[nid] = (kind, tid)

    use = collections.Counter(n for w in ways for n in set(w["nodes"]))
    way_ends = {w["nodes"][0] for w in ways} | {w["nodes"][-1] for w in ways}

    assign_inside(stations, "S")
    before_plants = set(node_term)
    assign_inside(plants, "P")
    # Day 3: a plant polygon only terminates a line that ends (or branches) inside it.
    for nid in [n for n, t in node_term.items() if t[0] == "P" and n not in before_plants]:
        if nid not in way_ends and use[nid] < 2:
            del node_term[nid]
            stats["plant_pass_through_nodes_ignored"] += 1

    # ---- Day 4: snap dangling way ends (no station nearby) to another line's node, or bridge end-to-end gaps
    st_geoms = [s["geom"] for s in stations]
    st_tree = STRtree(st_geoms) if st_geoms else None
    near_m = CFG["endpoint_matching"]["nearest_station_m"]
    wkv = {w["id"]: set(w["kvs"]) for w in ways}
    node_ways = collections.defaultdict(set)
    for w in ways:
        for nid in w["nodes"]:
            node_ways[nid].add(w["id"])

    def kv_ok(a_ways, b_ways):
        ka = set().union(*(wkv[x] for x in a_ways)) if a_ways else set()
        kb_ = set().union(*(wkv[x] for x in b_ways)) if b_ways else set()
        if not CFG["dangling_snap"]["require_voltage_match"] or not ka or not kb_:
            return True
        return bool(ka & kb_)

    def has_station_nearby(nid):
        if st_tree is None:
            return False
        p = Point(xy(node_ll[nid][1], node_ll[nid][0]))
        kvs = set().union(*(wkv[x] for x in node_ways[nid]))
        for t_i in st_tree.query(p, predicate="dwithin", distance=near_m):
            st = stations[int(t_i)]
            if not kvs or not st["tag_kvs"] or kvs & set(st["tag_kvs"]):
                return True
        return False

    from scipy.spatial import cKDTree
    all_xy = np.array([xy(node_ll[n][1], node_ll[n][0]) for n in node_ids])
    kdt = cKDTree(all_xy)
    idx_of = {n: i for i, n in enumerate(node_ids)}
    cands = [n for n in way_ends if n not in node_term and use[n] == 1 and not has_station_nearby(n)]
    cand_set = set(cands)
    alias = {}
    snap_rows = []
    for n in sorted(cands):
        if n in alias:
            continue
        here = all_xy[idx_of[n]]
        best = None
        for j in kdt.query_ball_point(here, CFG["dangling_snap"]["to_line_node_m"]):
            m = node_ids[j]
            if m == n or node_ways[m] & node_ways[n] or m in cand_set:
                continue
            if not kv_ok(node_ways[n], node_ways[m]):
                continue
            d = float(np.hypot(*(all_xy[j] - here)))
            if best is None or d < best[0]:
                best = (d, m, "snap_to_line")
        if best is None:
            for j in kdt.query_ball_point(here, CFG["dangling_snap"]["gap_bridge_m"]):
                m = node_ids[j]
                if m == n or m not in cand_set or m in alias or node_ways[m] & node_ways[n]:
                    continue
                if not kv_ok(node_ways[n], node_ways[m]):
                    continue
                d = float(np.hypot(*(all_xy[j] - here)))
                if best is None or d < best[0]:
                    best = (d, m, "gap_bridge")
        if best:
            d, m, rule = best
            alias[n] = m
            use[m] += 1
            stats[f"dangling_{rule}"] += 1
            snap_rows.append([n, m, rule, round(d, 1), ";".join(map(str, sorted(node_ways[n]))), ";".join(map(str, sorted(node_ways[m])))])

    # ---- split ways into segments at stations and shared nodes
    segs = []
    for w in ways:
        nodes = w["nodes"]
        n = len(nodes)
        brk = [i for i in range(n) if i in (0, n - 1) or nodes[i] in node_term or use[nodes[i]] >= 2]
        for i, j in zip(brk, brk[1:]):
            ti, tj = node_term.get(nodes[i]), node_term.get(nodes[j])
            if ti and tj and ti == tj:
                stats["segment_skipped_inside_station"] += 1
                continue
            L = sum(hav_m(*node_ll[nodes[k]], *node_ll[nodes[k + 1]]) for k in range(i, j))
            segs.append({"way": w, "a": alias.get(nodes[i], nodes[i]), "b": alias.get(nodes[j], nodes[j]),
                         "len_m": L, "n_pts": j - i + 1})
    stats["segments"] = len(segs)

    # ---- resolve raw endpoints
    deg = collections.Counter()
    for s in segs:
        for e in ("a", "b"):
            if s[e] not in node_term:
                deg[s[e]] += 1

    st_by_id = {s["id"]: s for s in stations}
    resolved = {}

    def terminal(nid, seg_kvs):
        if nid in node_term:
            k, tid = node_term[nid]
            return (k, tid), ("station_polygon" if k == "S" else "plant_polygon")
        if deg[nid] >= 2:
            return ("J", nid), "shared_node"
        key = (nid, tuple(seg_kvs))
        if key in resolved:
            return resolved[key]
        p = Point(xy(node_ll[nid][1], node_ll[nid][0]))
        best = None
        if st_tree is not None:
            for t_i in st_tree.query(p, predicate="dwithin", distance=near_m):
                st = stations[int(t_i)]
                ok = (not seg_kvs) or (not st["tag_kvs"]) or bool(set(seg_kvs) & set(st["tag_kvs"]))
                if CFG["endpoint_matching"]["require_voltage_match_for_nearest"] and not ok:
                    continue
                d = st["geom"].distance(p)
                if best is None or d < best[0]:
                    best = (d, st["id"])
        res = (("S", best[1]), f"nearest_station_{int(best[0])}m") if best else (("D", nid), "dangling")
        resolved[key] = res
        return res

    edges = []  # AC + DC, one per (segment, kv)
    for s in segs:
        w = s["way"]
        kv_list = w["kvs"] or [None]
        per_c = max(1, w["circuits"] // len(kv_list)) if len(kv_list) > 1 else w["circuits"]
        for kv in kv_list:
            ta, ra = terminal(s["a"], [kv] if kv else [])
            tb, rb = terminal(s["b"], [kv] if kv else [])
            for nid, t, r in ((s["a"], ta, ra), (s["b"], tb, rb)):
                stats[f"endpoint_rule:{r.split('_')[0] if r.startswith('nearest') else r}"] += 1
                log.append([w["id"], nid, kv or "", t[0], t[1], r])
            edges.append({
                "way": w["id"], "u": ta, "v": tb, "kv": kv, "kv_src": "tag" if kv else "", "circuits": per_c,
                "circuits_src": w["circuits_src"], "len_m": s["len_m"], "hvdc": w["hvdc"],
                "cable": w["power"] == "cable", "name": w["name"],
            })

    # ---- voltage inference for untagged AC edges
    def station_levels(t):
        # Day 3: station tag voltages plus voltages of incident lines whose voltage is TAGGED.
        # Inferred line voltages are never counted, so an inference cannot cascade through stations.
        if t[0] != "S":
            return set()
        return set(st_by_id[t[1]]["tag_kvs"]) | {e["kv"] for e in inc[t] if e["kv"] and e["kv_src"] == "tag"}

    inc = collections.defaultdict(list)
    for e in edges:
        inc[e["u"]].append(e)
        inc[e["v"]].append(e)
    if infer:
        changed = True
        while changed:
            changed = False
            for e in edges:
                if e["kv"] or e["hvdc"]:
                    continue
                cand, rule = None, ""
                for t in (e["u"], e["v"]):
                    if t[0] == "J":
                        ks = {o["kv"] for o in inc[t] if o is not e and o["kv"]}
                        if len(ks) == 1:
                            cand, rule = ks.pop(), "junction_neighbour"
                            break
                if cand is None and e["u"][0] in "SP" and e["v"][0] in "SP":
                    inter = station_levels(e["u"]) & station_levels(e["v"])
                    if len(inter) == 1:
                        cand, rule = inter.pop(), "common_station_level"
                if cand is None:
                    for t in (e["u"], e["v"]):
                        lv = station_levels(t)
                        if t[0] == "S" and len(lv) == 1:
                            cand, rule = next(iter(lv)), "single_level_station"
                            break
                if cand is not None:
                    e["kv"], e["kv_src"] = cand, rule
                    changed = True
    unknown = [e for e in edges if not e["kv"] and not e["hvdc"]]
    stats["edges_unknown_kv"] = len(unknown)
    stats["km_unknown_kv"] = round(sum(e["len_m"] for e in unknown) / 1000, 1)
    for e in edges:
        if e["kv_src"] and e["kv_src"] != "tag":
            stats[f"kv_inferred:{e['kv_src']}"] += 1

    ac = [e for e in edges if e["kv"] and not e["hvdc"]]
    dc_raw = [e for e in edges if e["hvdc"]]
    # Day 3: collapse DC pieces joined at plain junctions into end-to-end links between stations.
    D = nx.MultiGraph()
    for e in dc_raw:
        D.add_edge(e["u"], e["v"], len_m=e["len_m"], ways=str(e["way"]), kv=e["kv"], name=e["name"])
    for n in [n for n in D.nodes if n[0] == "J"]:
        if D.degree(n) == 2 and D.number_of_edges(n, n) == 0:
            (a_, _, d1), (b_, _, d2) = [(nb, n, d) for _, nb, d in D.edges(n, data=True)]
            D.remove_node(n)
            D.add_edge(a_, b_, len_m=d1["len_m"] + d2["len_m"], ways=d1["ways"] + ";" + d2["ways"], kv=d1["kv"], name=d1["name"] or d2["name"])
    dc = [{"u": u, "v": v, "kv": d["kv"], "len_m": d["len_m"], "way": d["ways"], "name": d["name"]} for u, v, d in D.edges(data=True)]
    stats["dc_pieces_raw"] = len(dc_raw)
    stats["dc_links_after_collapse"] = len(dc)

    # ---- buses, then collapse degree-2 junctions (series joints)
    def bkey(t, kv):
        return f"{t[0]}:{t[1]}@{kv}"

    G = nx.MultiGraph()
    for i, e in enumerate(ac):
        G.add_edge(bkey(e["u"], e["kv"]), bkey(e["v"], e["kv"]), key=i, **e, ways=str(e["way"]))
    collapsed = 0
    quirks = []
    for n in [n for n in G.nodes if n.startswith("J:")]:
        if G.degree(n) == 2 and G.number_of_edges(n, n) == 0:
            (u1, _, k1, d1), (u2, _, k2, d2) = [(nb, n, k, d) for _, nb, k, d in G.edges(n, keys=True, data=True)]
            if u1 == n or u2 == n:
                continue
            new = dict(d1)
            new["len_m"] = d1["len_m"] + d2["len_m"]
            # Day 4: across a series joint, a tagged circuit count beats the untagged default of 1.
            if d1["circuits_src"] == "default1" and d2["circuits_src"] != "default1":
                new["circuits"], new["circuits_src"] = d2["circuits"], d2["circuits_src"] + "(carried)"
            elif d2["circuits_src"] == "default1" and d1["circuits_src"] != "default1":
                new["circuits"], new["circuits_src"] = d1["circuits"], d1["circuits_src"] + "(carried)"
            else:
                new["circuits"] = min(d1["circuits"], d2["circuits"])
            new["ways"] = d1["ways"] + ";" + d2["ways"]
            if d1["circuits"] != d2["circuits"]:
                stats["series_merge_circuit_mismatch"] += 1
                quirks.append(["circuit_mismatch", n, d1["kv"], f"{d1['ways']} ({d1['circuits']}c, {d1['circuits_src']})",
                               f"{d2['ways']} ({d2['circuits']}c, {d2['circuits_src']})", round((d1["len_m"] + d2["len_m"]) / 1000, 2)])
            G.remove_node(n)
            G.add_edge(u1, u2, **new)
            collapsed += 1
    stats["series_joints_collapsed"] = collapsed
    loops = list(nx.selfloop_edges(G, keys=True, data=True))
    for u, v, k, d in loops:
        quirks.append(["self_loop", u, d["kv"], d["ways"], d["name"], round(d["len_m"] / 1000, 2)])
    G.remove_edges_from([(u, v, k) for u, v, k, _ in loops])
    stats["self_loops_dropped"] = len(loops)

    # transformer stubs between adjacent voltage levels of each station/plant
    levels = collections.defaultdict(set)
    for n in G.nodes:
        t, kv = n.rsplit("@", 1)
        if t[0] in "SP":
            levels[t].add(int(kv))
    trafos = []
    for t, kvs in levels.items():
        ks = sorted(kvs, reverse=True)
        for hi, lo in zip(ks, ks[1:]):
            trafos.append((f"{t}@{hi}", f"{t}@{lo}", hi, lo))
            G.add_edge(f"{t}@{hi}", f"{t}@{lo}", kind="transformer")

    # ---- bus table
    plant_by_id = {p["id"]: p for p in plants}
    ke_re = re.compile(CFG["ke_tagging"]["operator_regex"])
    kr = CFG["ke_region"]
    ngc_re = re.compile(kr["exclude_operator_regex"])
    buses = []
    for n in G.nodes:
        t, kv = n.rsplit("@", 1)
        kind, ref = t.split(":", 1)
        kv = int(kv)
        if kind == "S":
            st = st_by_id[ref]
            lat, lon, name, prov, op = st["lat"], st["lon"], st["name"], st["prov"], st["operator"]
        elif kind == "P":
            pl = plant_by_id[ref]
            lat, lon, name, prov, op = pl["lat"], pl["lon"], pl["name"], "plant", pl["operator"]
        else:
            lat, lon = node_ll[int(ref)]
            name, op = "", ""
            prov = "tee_junction" if kind == "J" else "dangling_end"
        ke = bool(ke_re.search(op or "")) or (
            kr["lat"][0] <= lat <= kr["lat"][1] and kr["lon"][0] <= lon <= kr["lon"][1]
            and kv <= kr["max_kv"] and not ngc_re.search(op or ""))
        buses.append({"bus": n, "kind": kind, "ref": ref, "kv": kv, "prov": prov, "name": name,
                      "lat": round(lat, 6), "lon": round(lon, 6), "ke": int(ke)})
    bus_by = {b["bus"]: b for b in buses}

    # ---- components
    comps = sorted(nx.connected_components(G), key=len, reverse=True)
    main = comps[0] if comps else set()
    for b in buses:
        b["in_main"] = int(b["bus"] in main)
    comp_rows = []
    for ci, c in enumerate(comps[:15]):
        km = sum(d.get("len_m", 0) for u, v, d in G.subgraph(c).edges(data=True)) / 1000
        kvs = collections.Counter(bus_by[n]["kv"] for n in c)
        gens = sum(1 for n in c if bus_by[n]["prov"] == "plant")
        comp_rows.append((ci, len(c), round(km, 1), dict(sorted(kvs.items(), reverse=True)), gens))

    per_kv = {}
    for kv in sorted({b["kv"] for b in buses}, reverse=True):
        H = nx.Graph()
        H.add_nodes_from(n for n in G.nodes if bus_by[n]["kv"] == kv)
        H.add_edges_from((u, v) for u, v, d in G.edges(data=True) if d.get("kind") != "transformer" and bus_by[u]["kv"] == kv)
        cs = sorted(nx.connected_components(H), key=len, reverse=True)
        per_kv[kv] = (H.number_of_nodes(), len(cs), [len(c) for c in cs[:5]], cs[0] if cs else set())

    # ---- branch table
    branches = []
    for u, v, d in G.edges(data=True):
        if d.get("kind") == "transformer":
            continue
        branches.append({"from": u, "to": v, "kv": d["kv"], "kv_src": d["kv_src"], "circuits": d["circuits"],
                         "circuits_src": d["circuits_src"], "len_km": round(d["len_m"] / 1000, 3),
                         "cable": int(d["cable"]), "ways": d["ways"], "name": d["name"]})

    # ---- S1 (provisional) and 500 kV backbone check
    s1 = [b for b in buses if b["in_main"] and b["kv"] >= min_kv and b["prov"] in CFG["s1_counted_provenance"]]
    s1_noke = [b for b in s1 if not b["ke"]]
    main500 = per_kv.get(500, (0, 0, [], set()))[3]
    backbone = []
    hints = {k: v for k, v in CFG.get("station_name_hints", {}).items() if not k.startswith("_")}
    for st in stations:
        st["hint"] = "; ".join(hints[m]["name"] + " [hint]" for m in st["members"].split(";") if m in hints)

    def norm(s):
        return re.sub(r"[^a-z0-9]", "", s.lower())

    st500 = [st for st in stations if f"S:{st['id']}@500" in bus_by]
    for label, aliases in NGC_500KV.items():
        hits = [st for st in st500 if any(norm(a) in norm(st["name"] + " " + st["hint"]) for a in aliases if norm(a))]
        hits = [st for st in hits if not (label in ("Guddu",) and "747" in st["hint"])]
        backbone.append((label, [f"{h['id']} {h['name'] or '(unnamed)'}{' / ' + h['hint'] if h['hint'] else ''}" for h in hits],
                         any(f"S:{h['id']}@500" in main500 for h in hits)))

    # ---- km by voltage
    km = collections.defaultdict(lambda: [0.0, 0.0])
    for br in branches:
        km[br["kv"]][0] += br["len_km"]
        km[br["kv"]][1] += br["len_km"] * br["circuits"]

    # ---- write outputs
    def wcsv(name, rows, cols):
        with open(out_dir / name, "w", newline="", encoding="utf-8") as f:
            wr = csv.writer(f)
            wr.writerow(cols)
            for r in rows:
                wr.writerow([r[c] for c in cols] if isinstance(r, dict) else r)

    wcsv("buses.csv", buses, ["bus", "kind", "ref", "kv", "prov", "name", "lat", "lon", "ke", "in_main"])
    wcsv("branches.csv", branches, ["from", "to", "kv", "kv_src", "circuits", "circuits_src", "len_km", "cable", "ways", "name"])
    wcsv("transformers.csv", trafos, ["hv_bus", "lv_bus", "hv_kv", "lv_kv"])
    # Day 5: each DC terminal is tied to the highest-voltage AC bus of its converter station (PowerModels dcline f_bus/t_bus).
    def ac_bus(t):
        kvs = sorted((int(b["kv"]) for b in buses if b["kind"] == t[0] and b["ref"] == t[1]), reverse=True)
        return f"{t[0]}:{t[1]}@{kvs[0]}" if kvs else ""

    wcsv("dclines.csv", [[e["way"], f"{e['u'][0]}:{e['u'][1]}", f"{e['v'][0]}:{e['v'][1]}", e["kv"] or "", round(e["len_m"] / 1000, 2), e["name"],
                          ac_bus(e["u"]), ac_bus(e["v"])] for e in dc],
         ["way", "from", "to", "kv", "len_km", "name", "ac_from", "ac_to"])
    wcsv("stations.csv", [{k: s[k] for k in ("id", "name", "prov", "tag_kvs", "n_members", "members", "subtypes", "operator", "lat", "lon", "all_names")} for s in stations],
         ["id", "name", "prov", "tag_kvs", "n_members", "members", "subtypes", "operator", "lat", "lon", "all_names"])
    wcsv("plants.csv", plants, ["id", "osm", "name", "source", "operator", "lat", "lon", "all_names"])
    wcsv("match_log.csv", log, ["way", "osm_node", "kv", "term_kind", "term_ref", "rule"])
    wcsv("snaps.csv", snap_rows, ["dangling_node", "snapped_to_node", "rule", "dist_m", "ways_from", "ways_to"])
    wcsv("quirks.csv", quirks, ["type", "bus", "kv", "detail_a", "detail_b", "len_km"])

    # ---- report
    L = []
    L.append(f"# Topology build — {'with voltage inference' if infer else 'explicit voltage tags only'}\n")
    L.append(f"OSM snapshot (Overpass `timestamp_osm_base`): {osm_base}. Data © OpenStreetMap contributors, ODbL 1.0.\n")
    L.append("## Inputs and rule counts\n")
    for k in sorted(stats):
        L.append(f"- {k}: {stats[k]}")
    L.append("\n## Buses by voltage × provenance\n")
    prov_order = ["substation", "plant", "converter", "tee_junction", "dangling_end"]
    tab = collections.Counter((b["kv"], b["prov"]) for b in buses)
    L.append("| kV | " + " | ".join(prov_order) + " | total | in main component |")
    L.append("|---|" + "---|" * (len(prov_order) + 2))
    for kv in sorted({b["kv"] for b in buses}, reverse=True):
        row = [tab[(kv, p)] for p in prov_order]
        inm = sum(1 for b in buses if b["kv"] == kv and b["in_main"])
        L.append(f"| {kv} | " + " | ".join(map(str, row)) + f" | {sum(row)} | {inm} |")
    inferred_only = collections.Counter()
    for n in G.nodes:
        srcs = [d.get("kv_src") for _, _, d in G.edges(n, data=True) if d.get("kind") != "transformer"]
        if srcs and all(s != "tag" for s in srcs):
            inferred_only[bus_by[n]["kv"]] += 1
    L.append("\nBuses whose every line has an inferred (not tagged) voltage: "
             + (", ".join(f"{kv} kV: {c}" for kv, c in sorted(inferred_only.items(), reverse=True)) or "none"))
    L.append(f"\nTransformer stubs (adjacent levels within a station/plant): {len(trafos)}. DC links: {len(dc)} (from {stats['dc_pieces_raw']} raw pieces).")
    for e in dc:
        def tname(t):
            if t[0] == "S":
                return f"{t[1]} {st_by_id[t[1]]['name']}"
            return f"{t[0]}:{t[1]}"
        L.append(f"- {tname(e['u'])} ↔ {tname(e['v'])}: {e['len_m'] / 1000:,.1f} km, {len(str(e['way']).split(';'))} OSM ways")
    L.append("\n## Line km by voltage (AC branches after series collapse)\n")
    L.append("| kV | route km | circuit km | branches |")
    L.append("|---|---|---|---|")
    nb = collections.Counter(br["kv"] for br in branches)
    for kv in sorted(km, reverse=True):
        L.append(f"| {kv} | {km[kv][0]:,.0f} | {km[kv][1]:,.0f} | {nb[kv]} |")
    L.append(f"\nUnknown-voltage edges left out: {stats['edges_unknown_kv']} ({stats['km_unknown_kv']} km).")
    L.append("\n## Connected components (AC branches + transformer stubs)\n")
    L.append(f"Total components: {len(comps)}. Largest 15:\n")
    L.append("| # | buses | km | buses by kV | plant buses |")
    L.append("|---|---|---|---|---|")
    for ci, n_, km_, kvs, gens in comp_rows:
        L.append(f"| {ci} | {n_} | {km_:,} | {kvs} | {gens} |")
    L.append("\n## Per-voltage connectivity (no transformers)\n")
    L.append("| kV | buses | components | 5 largest |")
    L.append("|---|---|---|---|")
    for kv, (nn, nc, top, _) in per_kv.items():
        L.append(f"| {kv} | {nn} | {nc} | {top} |")
    L.append("\n## Provisional S1 (gate counts buses at ≥66 kV in the main component with provenance substation/plant/converter)\n")
    L.append(f"- With K-Electric: **{len(s1)}**")
    L.append(f"- Without K-Electric (operator tag or Karachi bbox ≤220 kV): **{len(s1_noke)}**")
    L.append("- Provisional: Days 3–4 still add station splitting checks, voltage fixes and duplicate collapse.")
    L.append("\n## K-Electric region (working definition in config `ke_region`, [VERIFY])\n")
    ke_tab = collections.Counter((b["kv"], b["prov"]) for b in buses if b["ke"] and b["in_main"])
    L.append("KE buses in the main component by kV (substation / plant / tee / dangling); PER FY2024-25 KE grid stations: 500 kV 1, 220 kV 12, 132 kV 62, 66 kV 3.\n")
    for kv in sorted({k for k, _ in ke_tab}, reverse=True):
        L.append(f"- {kv} kV: substation {ke_tab[(kv, 'substation')]}, plant {ke_tab[(kv, 'plant')]}, "
                 f"tee {ke_tab[(kv, 'tee_junction')]}, dangling {ke_tab[(kv, 'dangling_end')]}")
    iface = []
    for u, v, d in G.edges(data=True):
        if bus_by[u]["ke"] != bus_by[v]["ke"]:
            ke_side, other = (u, v) if bus_by[u]["ke"] else (v, u)
            iface.append((other, ke_side, d.get("kind", "line"), d.get("kv", ""), round(d.get("len_m", 0) / 1000, 1)))
    L.append(f"\nInterface edges between KE and the rest of the main grid: {len(iface)} (these carry TSEP's 'Export to KE').\n")
    L.append("| NGC-side bus | KE-side bus | type | kV | km |")
    L.append("|---|---|---|---|---|")
    for o, k, t, kv, km_ in sorted(iface):
        L.append(f"| {o} {bus_by[o]['name']} | {k} {bus_by[k]['name']} | {t} | {kv} | {km_} |")
    L.append("\n## Snapping and quirks (Day 4)\n")
    L.append(f"- Dangling ends snapped to another line's node (≤{CFG['dangling_snap']['to_line_node_m']} m): {stats['dangling_snap_to_line']}; "
             f"end-to-end gaps bridged (≤{CFG['dangling_snap']['gap_bridge_m']} m): {stats['dangling_gap_bridge']}. Each in snaps.csv.")
    qt = collections.Counter(q[0] for q in quirks)
    L.append(f"- Quirks logged in quirks.csv: {dict(qt)}.")
    L.append("\n## 500 kV backbone check (PER FY2024-25 Figure 1, 20 NGC stations)\n")
    found = sum(1 for _, h, _ in backbone if h)
    inmain = sum(1 for _, _, m in backbone if m)
    L.append(f"Found as a 500 kV bus by name: {found}/20; in the largest 500 kV component: {inmain}/20.\n")
    L.append("| PER name | matched OSM stations (500 kV bus) | in main 500 kV component |")
    L.append("|---|---|---|")
    for label, hits, m in backbone:
        L.append(f"| {label} | {'; '.join(hits) if hits else '—'} | {'yes' if m else 'no'} |")
    (out_dir / "report.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print("\n".join(L))


if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-infer", action="store_true")
    args = ap.parse_args()
    build(infer=not args.no_infer)
