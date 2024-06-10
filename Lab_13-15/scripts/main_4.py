import folium
import geojson
from shapely.wkt import loads

# Query to get the nearest parks to Los Angeles
query_nearest_parks_to_la = """
SELECT p.name, SDO_GEOM.SDO_DISTANCE(p.geom, c.location, 0.005, 'unit=KM') as distance, SDO_UTIL.TO_WKTGEOMETRY(p.geom)
FROM us_parks p, us_cities c
WHERE c.city = 'Los Angeles'
ORDER BY distance
FETCH FIRST 5 ROWS ONLY
"""

# Execute the query and fetch the results
results = cursor.execute(query_nearest_parks_to_la).fetchall()

# Initialize the map centered on Los Angeles
m = folium.Map(location=[34.0522, -118.2437], zoom_start=12)

# Define style for the parks
style = {"fillColor": "green", "color": "darkgreen"}

# Initialize an empty list to store GeoJSON features
features = []

# Process the query results
for row in results:
    park_name = row[0]
    park_distance = row[1]
    park_geom_wkt = row[2]

    # Convert WKT to Shapely geometry
    park_geom = loads(park_geom_wkt)

    # Create a GeoJSON feature with the park's geometry and properties
    park_geojson_geom = geojson.Feature(
        geometry=park_geom, properties={"name": park_name, "distance_km": park_distance}
    )

    # Add the feature to the list
    features.append(park_geojson_geom)

    # Add a marker to the map for each park with a popup showing its name and distance
    folium.Marker(
        location=[park_geom.centroid.y, park_geom.centroid.x],
        popup=f"<strong>{park_name}</strong><br>Distance: {park_distance:.2f} km",
        icon=folium.Icon(color="green"),
    ).add_to(m)

# Create a GeoJSON FeatureCollection
feature_collection = geojson.FeatureCollection(features)

# Add the GeoJSON data to the map with styling
folium.GeoJson(feature_collection, style_function=lambda x: style).add_to(m)
