import folium
import geojson
from shapely.wkt import loads

# Initialize an empty folium map
m = folium.Map()

# Define the SQL query to find the longest river and counties that intersect with it
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

# Execute the SQL query and fetch all results
# This returns the geometries of counties that intersect with the longest river in WKT format
results = cursor.execute(query).fetchall()

# Define the style for the GeoJSON features
style = {"fillColor": "blue", "color": "red"}

l = []
for row in results:
    # Create a GeoJSON feature with the geometry and empty properties and add to list
    g = geojson.Feature(geometry=row[0], properties={})
    l.append(g)

# Create a GeoJSON FeatureCollection from the list of features
feature_collection = geojson.FeatureCollection(l)

# Add the GeoJSON data to the folium map with the specified style
folium.GeoJson(feature_collection, style_function=lambda x: style).add_to(m)
