import folium
import geojson
from shapely import wkt
from shapely.geometry import shape

# Initialize map
m = folium.Map()

# New query to get the MBR of each state geometry
query = """
SELECT SDO_UTIL.TO_WKTGEOMETRY(SDO_GEOM.SDO_MBR(c.geom))
FROM us_states c
"""

# Execute the query and fetch results
results = cursor.execute(query).fetchall()

# Define style for GeoJson
style = {"fillColor": "blue", "color": "red"}

# Process the query results into GeoJSON features
features = []
for row in results:
    # Convert WKT to GeoJSON geometry
    geom = wkt.loads(row[0])
    geojson_geom = geojson.Feature(geometry=shape(geom), properties={})
    features.append(geojson_geom)

# Create a GeoJSON FeatureCollection
feature_collection = geojson.FeatureCollection(features)

# Add the GeoJSON data to the map with styling
folium.GeoJson(feature_collection, style_function=lambda x: style).add_to(m)
