import json, math

boundary = [(p[1], p[0]) for p in json.load(open('tf.json'))[0]['geojson']['coordinates'][0]]
roads = json.load(open('roads.json'))['elements']

blat = [p[0] for p in boundary]; blng = [p[1] for p in boundary]
clat = (min(blat)+max(blat))/2; clng = (min(blng)+max(blng))/2
k = math.cos(math.radians(clat))

# frame: fit boundary with padding, target aspect W:H = 1000:1250
bw = (max(blng)-min(blng))*k; bh = max(blat)-min(blat)
PAD = 1.18
H = bh*PAD
W = H*(1000/1250)
if W < bw*PAD:
    W = bw*PAD; H = W*(1250/1000)
lat0 = clat + H/2; lat1 = clat - H/2
lng0 = clng - (W/k)/2; lng1 = clng + (W/k)/2
SW, SH = 1000.0, 1250.0

def prj(lat, lng):
    x = (lng-lng0)/(lng1-lng0)*SW
    y = (lat0-lat)/(lat0-lat1)*SH
    return x, y

def path(pts, close=False):
    d = 'M' + 'L'.join('%.1f %.1f' % prj(la, ln) for la, ln in pts)
    return d + ('Z' if close else '')

CLASSES = {
    'primary':      ('major', 14.0),
    'primary_link': ('major', 9.0),
    'trunk':        ('major', 14.0),
    'secondary':    ('major', 11.0),
    'tertiary':     ('mid',   9.0),
    'unclassified': ('mid',   7.0),
    'residential':  ('mid',   7.0),
    'service':      ('minor', 4.0),
    'track':        ('minor', 3.0),
    'living_street':('minor', 5.0),
}

def inside(lat, lng):
    # ray casting
    c = False; n = len(boundary)
    for i in range(n):
        a = boundary[i]; b = boundary[(i+1) % n]
        if (a[0] > lat) != (b[0] > lat):
            x = (b[1]-a[1])*(lat-a[0])/(b[0]-a[0]) + a[1]
            if lng < x: c = not c
    return c

buckets = {'major': [], 'mid': [], 'minor': [], 'foot': []}
labels = []
for w in roads:
    tags = w.get('tags', {}); hw = tags.get('highway')
    geom = w.get('geometry') or []
    if len(geom) < 2: continue
    pts = [(g['lat'], g['lon']) for g in geom]
    if hw in ('footway', 'path', 'pedestrian', 'steps', 'cycleway'):
        buckets['foot'].append(path(pts)); continue
    if hw not in CLASSES: continue
    cls, wdt = CLASSES[hw]
    buckets[cls].append(path(pts))
    name = tags.get('name')
    if name and cls in ('major', 'mid'):
        # longest segment midpoint, inside boundary preferred
        best = None
        for i in range(len(pts)-1):
            a, b = pts[i], pts[i+1]
            dx = (b[1]-a[1])*k; dy = b[0]-a[0]
            L = math.hypot(dx, dy)
            mlat = (a[0]+b[0])/2; mlng = (a[1]+b[1])/2
            score = L * (3.0 if inside(mlat, mlng) else 1.0)
            if best is None or score > best[0]:
                ang = math.degrees(math.atan2(-dy, dx))
                if ang > 90: ang -= 180
                if ang < -90: ang += 180
                best = (score, mlat, mlng, ang, L, inside(mlat, mlng))
        if best and best[4] > 0.0006:
            labels.append({'name': name, 'lat': best[1], 'lng': best[2],
                           'rot': round(best[3], 1), 'in': best[5],
                           'cls': cls})

# de-dupe labels by name, keep the inside/longest one
seen = {}
for L in labels:
    key = L['name']
    if key not in seen or (L['in'], 1) > (seen[key]['in'], 0):
        seen[key] = L
labels = list(seen.values())

out = {
  'frame': {'lat0': lat0, 'lat1': lat1, 'lng0': lng0, 'lng1': lng1, 'w': SW, 'h': SH},
  'boundary': path(boundary, True),
  'boundaryLL': boundary,
  'roads': buckets,
  'labels': [{**L, 'x': round(prj(L['lat'], L['lng'])[0], 1),
                   'y': round(prj(L['lat'], L['lng'])[1], 1)} for L in labels],
}
json.dump(out, open('mapdata.json', 'w'), ensure_ascii=False)
print('frame lat %.5f..%.5f lng %.5f..%.5f' % (lat1, lat0, lng0, lng1))
for kk, v in buckets.items(): print(kk, len(v))
print('labels', len(labels))
for L in labels:
    if L['in']: print('  IN ', L['name'], L['x'], L['y'], L['rot'])
