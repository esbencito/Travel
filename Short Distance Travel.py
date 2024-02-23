import folium
from folium import features
import os

# Define the data for the capitals, including the country codes
capitals_data = [
    ('Taipei', 25.0330, 121.5654, 'TWN', 'Taiwan'),
    ('Hanoi', 21.0285, 105.8542, 'VNM', 'Vietnam'),
    ('Manila', 14.5995, 120.9842, 'PHL', 'Philippines'),
    ('Vientiane', 17.9757, 102.6331, 'LAO', 'Laos'),
    ('Phnom Penh', 11.5564, 104.9282, 'KHM', 'Cambodia'),
    ('Bangkok', 13.7563, 100.5018, 'THA', 'Thailand'),
    ('Naypyidaw', 19.7633, 96.0785, 'MMR', 'Myanmar'),
    ('Bandar Seri Begawan', 4.9031, 114.9398, 'BRN', 'Brunei'),
    ('Beijing', 39.9042, 116.4074, 'CHN', 'China'),
    ('Seoul', 37.5665, 126.9780, 'KOR', 'South Korea'),
    ('Pyongyang', 39.0392, 125.7625, 'PRK', 'North Korea'),
    ('Dhaka', 23.8103, 90.4125, 'BGD', 'Bangladesh'),
    ('Kuala Lumpur', 3.1390, 101.6869, 'MYS', 'Malaysia'),
    ('Thimphu', 27.4728, 89.6393, 'BTN', 'Bhutan'),
    ('Singapore', 1.3521, 103.8198, 'SGP', 'Singapore'),
    ('Ngerulmud', 7.5006, 134.6242, 'PLW', 'Palau'),
    ('Tokyo', 35.6895, 139.6917, 'JPN', 'Japan'),
    ('Ulaanbaatar', 47.8864, 106.9057, 'MNG', 'Mongolia'),
    ('Kathmandu', 27.7172, 85.3240, 'NPL', 'Nepal'),
    ('Jakarta', -6.2088, 106.8456, 'IDN', 'Indonesia')
]

# Initialize the Folium map centered around Hong Kong
m = folium.Map(location=[22.3193, 114.1694], zoom_start=5)

# Loop through capitals data and add markers
for name, lat, lon, code, country_name in capitals_data:
    folium.Marker(
        location=[lat, lon],
        tooltip=name,
        icon=folium.Icon(color='lightgray', icon='info-sign')
    ).add_to(m)

# Style function for GeoJSON layers
def style_function(feature):
    return {'fillColor': 'blue', 'color': 'black', 'weight': 1, 'fillOpacity': 0.6}

# Base URL for the GeoJSON files of other countries
base_url = 'https://raw.githubusercontent.com/johan/world.geo.json/master/countries/{}.geo.json'

# Special handling for Singapore and Palau within the loop
for name, lat, lon, code, country_name in capitals_data:
    try:
        if code == 'SGP':
            singapore_geojson_url = 'https://raw.githubusercontent.com/yinshanyang/singapore/master/maps/0-country.geojson'
            folium.GeoJson(singapore_geojson_url, name='Singapore', style_function=style_function).add_to(m)
        elif code == 'PLW':
            # Custom rectangle for Palau as previously defined
            # Insert the custom GeoJSON for Palau here
            palau_geojson_data = {
                "type": "FeatureCollection",
                "features": [{
                    "type": "Feature",
                    "properties": {"name": "Palau"},
                    "geometry": {
                      "type": "Polygon",
                     "coordinates": [[
                            [134.00012, 6.800],  # Bottom-left
                            [134.56012, 7.000],   # Top-left
                            [134.7434, 7.872],    # Top-right
                            [134.5434, 7.806],   # Bottom-right
                            [134.46012, 7.5006]   # Back to Bottom-left to close the polygon
                        ]]
                    }
                }]
            }
            folium.GeoJson(palau_geojson_data, name='Palau',style_function=style_function).add_to(m)
        else:
            # Use the base URL for other countries
            geojson_url = base_url.format(code)
            folium.GeoJson(geojson_url, name=country_name, style_function=style_function).add_to(m)
    except Exception as e:
        print(f"Failed to load {code}: {e}")

# Draw a circle around Hong Kong with a radius of 3500 km
folium.Circle(
    location=[22.3193, 114.1694],
    radius=3500000,
    color='blue',
    fill=True,
    fill_color='blue',
    fill_opacity=0.2,
    weight=1
).add_to(m)

# Correctly add a layer control to toggle countries
folium.LayerControl().add_to(m)

# Define Hong Kong's location
hk_location = [22.3193, 114.1694]

# Calculate an endpoint for the line, simplistically moving eastward
# This is a simplified calculation and may not accurately represent 3,500 km on the map's projection
radius_km = 3500
# Approximate conversion assuming uniform degree distance at this latitude
km_per_degree = 102.66
change_in_longitude = radius_km / km_per_degree
end_location = [hk_location[0], hk_location[1] + change_in_longitude]

# Add a dashed line for the radius
folium.PolyLine(
    locations=[hk_location, end_location],
    color='blue',
    weight=2,
    dash_array='5, 5',  # Creates a dashed line pattern
).add_to(m)

# Adding a label for the radius line
# Note: Folium doesn't support direct text labels on lines. As a workaround, you can use a Popup on a hidden marker.
radius_label_location = [((hk_location[0] + end_location[0]) / 2)+1, (hk_location[1] + end_location[1]) / 2]  # Midpoint

radius_marker = folium.Marker(
    location=radius_label_location,
    icon=folium.DivIcon(html='''
        <div style="font-size: 10pt; color: blue; width: 100px; white-space: nowrap;">5 hours flight</div>
    '''),
    popup='3,500 km'
)

radius_marker.add_to(m)

# Dynamically get the directory of the current script to save the map
script_dir = os.path.dirname(os.path.abspath(__file__))
map_file_path = os.path.join(script_dir, 'Travel Map.html')

m.save(map_file_path)