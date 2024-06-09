import folium
import geojson
from shapely import wkt
from shapely.geometry import shape

# Initialize the map centered on Texas
m = folium.Map(location=[31.0, -100.0], zoom_start=6)

# Query to get the longest river in Texas
query_longest_river_in_texas = """
SELECT r.name, SDO_GEOM.SDO_LENGTH(r.geom, 0.005, 'unit=KM') as length, SDO_UTIL.TO_WKTGEOMETRY(r.geom)
FROM us_rivers r, us_states s
WHERE s.state = 'Texas' AND SDO_ANYINTERACT(r.geom, s.geom) = 'TRUE'
ORDER BY length DESC
FETCH FIRST ROW ONLY
"""

# Execute the query and fetch the result
result = cursor.execute(query_longest_river_in_texas).fetchone()

# Extract river name, length, and geometry
river_name = result[0]
river_length = result[1]
river_geom_wkt = result[2]

# Convert WKT to GeoJSON geometry
river_geom = wkt.loads(river_geom_wkt)
river_geojson_geom = geojson.Feature(
    geometry=shape(river_geom),
    properties={"name": river_name, "length_km": river_length},
)

# Define style for the river
style = {"fillColor": "blue", "color": "red"}

# Create a GeoJSON FeatureCollection
feature_collection = geojson.FeatureCollection([river_geojson_geom])

# Add the GeoJSON data to the map with styling
folium.GeoJson(feature_collection, style_function=lambda x: style).add_to(m)

# Add a popup with the river name and length
popup_content = f"<strong>{river_name}</strong><br>Length: {river_length} km"
folium.Popup(popup_content).add_to(m)
