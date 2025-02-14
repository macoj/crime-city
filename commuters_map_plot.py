import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import networkx as nx
from lib.uk_lat_lng import uk_lat_lng  # Pre-defined UK city coordinates
from matplotlib.lines import Line2D

file_path = "data/population_matrix.csv"
df = pd.read_csv(file_path, index_col=0)

# Load and prepare the UK map
counties = gpd.read_file('lib/uk_admin_map_shapefile/Map_UK.shp')
counties = counties[counties["NAME_1"] != "Northern Ireland"]
counties = counties.to_crs(epsg=4326)

valid_cities = {city: coords for city, coords in uk_lat_lng.items() if coords}

# Create the plot with two subplots: map and legend
fig = plt.figure(figsize=(22, 22))
gs = fig.add_gridspec(1, 2, width_ratios=[4, 1])  # Adjust width ratios as needed
ax = fig.add_subplot(gs[0])
legend_ax = fig.add_subplot(gs[1])

ax.set_aspect("equal")

# Plot the UK map
counties.plot(ax=ax, color='whitesmoke', edgecolor='gainsboro')

# Set map boundaries
ax.set_xlim(-8.5, 2.5)
ax.set_ylim(49.5, 59.5)

# Define stronger colors
incoming_color = '#FF0000'  # Pure red
outgoing_color = '#00AA00'  # Stronger green

# Plot city nodes
for city, (lon, lat) in valid_cities.items():
    ax.scatter(lon, lat, s=df.loc[city, city] / 1000, color="blue", alpha=0.8)

# Create directed graph
G = nx.DiGraph()
for city1, coords1 in valid_cities.items():
    for city2, coords2 in valid_cities.items():
        if city1 != city2:
            weight = df.loc[city1, city2]
            if weight > 500:  # Threshold for visibility
                G.add_edge(city1, city2, weight=weight)

# Plot edges with different colors based on direction
for city1, city2, data_dict in G.edges(data=True):
    (lon1, lat1) = valid_cities[city1]
    (lon2, lat2) = valid_cities[city2]

    # Calculate the midpoint for the arrow
    mid_x = (lon1 + lon2) / 2
    mid_y = (lat1 + lat2) / 2

    # If flow is towards a larger city (incoming)
    if df.loc[city2, city2] > df.loc[city1, city1]:
        color = incoming_color
    # If flow is towards a smaller city (outgoing)
    else:
        color = outgoing_color

    # Plot the flow line with increased alpha
    ax.plot([lon1, lon2], [lat1, lat2],
            color=color, alpha=0.5,  # Increased alpha for stronger colors
            linewidth=data_dict["weight"] / 5000)

# Remove axes and frame
ax.set_xticks([])
ax.set_yticks([])
ax.set_frame_on(False)

# Create legend in the separate axis
legend_elements = [
    Line2D([0], [0], color=incoming_color, alpha=0.8, linewidth=3,
           label='Incoming Flow (towards larger cities)'),
    Line2D([0], [0], color=outgoing_color, alpha=0.8, linewidth=3,
           label='Outgoing Flow (towards smaller cities)'),
    plt.scatter([], [], c='blue', alpha=0.8, s=200,
                label='City Size (proportional to population)')
]

legend_ax.legend(handles=legend_elements, loc='center', frameon=True,
                 facecolor='white', edgecolor='none', fontsize=12)
legend_ax.axis('off')

plt.tight_layout()
plt.savefig("output/uk_city_flows.pdf", dpi=300, bbox_inches='tight', pad_inches=0)
plt.show()