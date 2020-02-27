import requests
import folium
import pandas

"""
My Location
"""
ip_request = requests.get('http://get.geojs.io/v1/ip.json')
my_ip = ip_request.json()['ip']
url = "http://get.geojs.io/v1/geo/"+my_ip+".json"
geo_request = requests.get(url)
geo_result = geo_request.json()
longitude = geo_result.get("longitude")
latitude = geo_result.get("latitude")
map = folium.Map(location=[latitude, longitude], zoom_start=6, tiles="Stamen Terrain")
fg0 = folium.FeatureGroup(name="My Location")
fg0.add_child(folium.Marker([latitude, longitude], popup=f"My Location : {latitude} {longitude}", icon=folium.Icon("white")))
map.add_child(fg0)

"""
Polygones & Colors
"""
fg1 = folium.FeatureGroup(name="Polygones & Countries Colors")
fg1.add_child(folium.GeoJson(data=open("world.json", encoding='utf-8-sig').read(),style_function=lambda x: {'fillColor': 'green' if x['properties']['POP2005'] <= 10000000 else 'orange' if 10000000 <= x['properties']['POP2005'] < 20000000 else 'red'}))
map.add_child(fg1)

"""
Earthquakes
"""
fg2 = folium.FeatureGroup(name="Earthquakes")
xl = pandas.ExcelFile("/home/saman/Webmap/Earthquakes.xlsx")
dfs = xl.sheet_names
html = """<h4>Earthquake information:</h4>
Richter: %s
<br>
%s
"""


def color_producer(mv):
    if mv < 5:
        return "green"
    elif mv <6 and mv >= 5:
        return "orange"
    else:
        return "red"


for i in dfs:
    df = pandas.read_excel("/home/saman/Webmap/Earthquakes.xlsx", sheet_name=i, header=None)
    df = df.drop(df.index[0:2], 0)
    df = df.drop(0, 1)
    for lat, lon, loc, Mv in zip(df[3], df[4], df[31], df[11]):
        iframe = folium.IFrame(html=html % (str(Mv), loc), width=200, height=100)
        fg2.add_child(folium.CircleMarker((lat, lon), popup=folium.Popup(iframe), fill=True, fill_color=color_producer(Mv), fill_opacity=0.7, tooltip="Earthquick", radius=6, color="grey", icon=folium.Icon(color_producer(Mv))))
map.add_child(fg2)
"""
Layer Control
"""
map.add_child(folium.LayerControl())
map.save("/home/saman/Webmap/Webmap.html")
