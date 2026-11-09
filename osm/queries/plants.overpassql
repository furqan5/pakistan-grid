[out:json][timeout:900][maxsize:1073741824];
area["ISO3166-1"="PK"][admin_level=2]->.pk;
(
  node["power"="plant"](area.pk);
  way["power"="plant"](area.pk);
  relation["power"="plant"](area.pk);
);
out body geom;
