import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.lines import Line2D

file_path = "data/population_matrix.csv"


def map_plot(ax):
    counties = gpd.read_file('lib/uk_admin_map_shapefile/Map_UK.shp')
    counties = counties[counties["NAME_1"] != "Northern Ireland"]
    counties = counties[counties["NAME_1"] != "Scotland"]
    counties = counties.to_crs(epsg=4326)
    counties.plot(ax=ax, color='whitesmoke', edgecolor='gainsboro')


df = pd.read_csv(file_path, index_col=0)

local_authorities = pd.read_csv("data/new/local_authorities.csv", delimiter=";")

lad_to_csp = pd.read_csv("data/new/lad_to_csp.csv", delimiter=";")

population_matrix = pd.read_csv("data/population_matrix.csv", delimiter=",")

local_authorities["lat"] = (
    local_authorities["lat"].astype(str).str.replace(",", ".").astype(float)
)
local_authorities["long"] = (
    local_authorities["long"].astype(str).str.replace(",", ".").astype(float)
)

valid_cities = {
    row["nice-name"]: (row["lat"], row["long"], row['lad_code'])
    for _, row in local_authorities.dropna(subset=["lat", "long", "lad_code"]).iterrows()
}

cities = population_matrix["City"].unique()

city_locations = {
    city: valid_cities[city]
    for city in cities if city in valid_cities
}

# city_sizes = population_matrix.set_index("City").sum(axis=1)
# city_sizes = {city: city_sizes[city] for city in cities if city in city_sizes}
# max_size = max(city_sizes.values()) if city_sizes else 1
# city_sizes = {city: (size / max_size) * 500 for city, size in city_sizes.items()}  # Scale size to a max of 500

fig = plt.figure(figsize=(22, 22))
gs = fig.add_gridspec(1, 2, width_ratios=[4, 1])  # Adjust width ratios as needed
ax = fig.add_subplot(gs[0])
legend_ax = fig.add_subplot(gs[1])
ax.set_aspect("equal")
map_plot(ax)

ax.set_xlim(-8.5, 2.5)
ax.set_ylim(49.5, 59.5)

for (city, (lon, lat, code)) in city_locations.items():
    ax.scatter(lon, lat, color="blue", alpha=0.6)

incoming_color = '#FF0000'  # Pure red
outgoing_color = '#00AA00'  # Stronger green

G = nx.DiGraph()
for city1, coords1 in city_locations.items():
    for city2, coords2 in city_locations.items():
        if city1 != city2:
            weight = df.loc[city1, city2]
            if weight > 500:
                G.add_edge(city1, city2, weight=weight)

for city1, city2, data_dict in G.edges(data=True):
    (lon1, lat1, _) = city_locations[city1]
    (lon2, lat2, _) = city_locations[city2]

    mid_x = (lon1 + lon2) / 2
    mid_y = (lat1 + lat2) / 2

    if df.loc[city2, city2] > df.loc[city1, city1]:
        color = incoming_color
    else:
        color = outgoing_color

    ax.plot([lon1, lon2], [lat1, lat2],
            color=color, alpha=0.5,  # Increased alpha for stronger colors
            linewidth=data_dict["weight"] / 5000)

ax.set_xticks([])
ax.set_yticks([])
ax.set_frame_on(False)

legend_elements = [
    Line2D([0], [0], color=incoming_color, alpha=0.8, linewidth=3,
           label='Incoming Flow (towards larger cities)'),
    Line2D([0], [0], color=outgoing_color, alpha=0.8, linewidth=3,
           label='Outgoing Flow (towards smaller cities)'),
    plt.scatter([], [], c='blue', alpha=0.8, s=200,
                label='City')
]

legend_ax.legend(handles=legend_elements, loc='upper right', frameon=True,
                 facecolor='white', edgecolor='none', prop={'family': 'Times New Roman', 'size': 32})  # Increased font size
legend_ax.axis('off')

plt.tight_layout()
plt.savefig("output/great_britain_commuting.pdf", dpi=300, bbox_inches='tight', pad_inches=0)
plt.show()
