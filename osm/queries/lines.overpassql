[out:json][timeout:900][maxsize:1073741824];
area["ISO3166-1"="PK"][admin_level=2]->.pk;
way["power"~"^(line|cable)$"](area.pk);
out body geom;
