[out:json][timeout:900][maxsize:1073741824];
area["ISO3166-1"="PK"][admin_level=2]->.pk;
(
  node["power"="substation"](area.pk);
  way["power"="substation"](area.pk);
  relation["power"="substation"](area.pk);
);
out body geom;
