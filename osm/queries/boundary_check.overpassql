[out:json][timeout:120];
area["ISO3166-1"="PK"][admin_level=2]->.pk;
(
  node(area.pk)["place"~"^(city|town)$"]["name:en"~"^(Muzaffarabad|Mirpur|Gilgit|Skardu)$"];
);
out tags center;
