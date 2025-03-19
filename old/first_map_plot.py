import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import networkx as nx
from old.uk_lat_lng import uk_lat_lng  # Pre-defined UK city coordinates

file_path = "../data/A.csv"
df = pd.read_csv(file_path, index_col=0)

counties = gpd.read_file('../lib/uk_admin_map_shapefile/Map_UK.shp')
counties = counties[counties["NAME_1"] != "Northern Ireland"]

counties = counties.to_crs(epsg=4326)

valid_cities = {city: coords for city, coords in uk_lat_lng.items() if coords}

fig, ax = plt.subplots(figsize=(18, 22))
ax.set_aspect("equal")

counties.plot(ax=ax, color='whitesmoke', edgecolor='gainsboro')

ax.set_xlim(-8.5, 2.5)
ax.set_ylim(49.5, 59.5)

for city, (lon, lat) in valid_cities.items():
    ax.scatter(lon, lat, s=df.loc[city, city] / 1000, color="blue", alpha=0.6)

G = nx.DiGraph()
for city1, coords1 in valid_cities.items():
    for city2, coords2 in valid_cities.items():
        if city1 != city2:
            weight = df.loc[city1, city2]
            if weight > 500:
                G.add_edge(city1, city2, weight=weight)

for city1, city2, data_dict in G.edges(data=True):
    (lon1, lat1) = valid_cities[city1]
    (lon2, lat2) = valid_cities[city2]
    ax.plot([lon1, lon2], [lat1, lat2],
            color="red", alpha=0.3, linewidth=data_dict["weight"] / 5000)

ax.set_xticks([])
ax.set_yticks([])
ax.set_frame_on(False)

plt.draw()
plt.savefig("uk_city_flows.pdf", dpi=300, bbox_inches='tight', pad_inches=0)
plt.show()
