[out:json][timeout:600][maxsize:536870912];
area["ISO3166-1"="PK"][admin_level=2]->.pk;
way["power"~"^(line|cable)$"](29.0,69.0,33.0,78.0)(area.pk);
out body geom;
