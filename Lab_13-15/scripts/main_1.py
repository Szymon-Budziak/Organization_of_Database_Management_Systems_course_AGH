import folium
import geojson
from shapely.wkt import loads

m = folium.Map()

query = """
WITH LongestRiver AS (
SELECT r.geom
FROM us_rivers as r
ORDER BY SDO_GEOM.SDO_LENGTH(r.geom, 0.005) DESC
FETCH FIRST 1 ROWS ONLY)

SELECT sdo_util.to_wktgeometry(c.geom)
FROM us_counties as c, LongestRiver as lr
WHERE SDO_ANYINTERACT (c.geom, lr.geom) =
'TRUE'
"""

r = loads(cursor.execute(query).fetchall())
style = {"fillColor": "blue", "color": "red"}

l = []
for row in r:
    g = geojson.Feature(geometry=row[0], properties={})
    l.append(g)

feature_collection = geojson.FeatureCollection(l)
folium.GeoJson(feature_collection, style_function=lambda x: style).add_to(m)
