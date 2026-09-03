# 地圖資料產生器

`build_mapdata.py` 會把台鳳里的里界與街道網轉成 `src/mapdata.json`。
原始資料需要先抓下來（只有換里、或街道有變動時才要重跑）：

```bash
# 1. 里界（OpenStreetMap Nominatim）
curl -A "taifeng-tnvr" \
  "https://nominatim.openstreetmap.org/search?q=%E5%8F%B0%E9%B3%B3%E9%87%8C%20%E5%BD%B0%E5%8C%96%E5%B8%82&format=jsonv2&polygon_geojson=1&limit=1" \
  > tf.json

# 2. 街道網（OpenStreetMap Overpass）
curl -X POST -d '[out:json][timeout:60];(way["highway"](24.0625,120.5905,24.0795,120.6080););out geom;' \
  https://overpass-api.de/api/interpreter > roads.json

# 3. 產生 mapdata.json
python3 build_mapdata.py
```

資料授權：© OpenStreetMap 貢獻者，ODbL。
