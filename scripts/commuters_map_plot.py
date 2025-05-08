import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.lines import Line2D

from config import PREPROCESSED_CSP_LOCATIONS, PREPROCESSED_POPULATION_MATRIX_CSV, SHOW_CSP_NAMES_MAP_PLOT, \
    PREPROCESSED_CSP_POPULATION_CSV, SCALE_CSP_NODES_BY_POPULATION_MAP_PLOT, NODE_SCALING_FACTOR_MAP_PLOT


def plot_commuting_map(output_path):
    def map_plot(ax):
        counties = gpd.read_file('lib/uk_admin_map_shapefile/Map_UK.shp')
        counties = counties[counties["NAME_1"] != "Northern Ireland"]
        counties = counties[counties["NAME_1"] != "Scotland"]
        counties = counties.to_crs(epsg=4326)
        counties.plot(ax=ax, color='whitesmoke', edgecolor='gainsboro')

    min_weight = 500
    figsize = (22, 22)

    df = pd.read_csv(PREPROCESSED_POPULATION_MATRIX_CSV, index_col=0)
    csps = pd.read_csv(PREPROCESSED_CSP_LOCATIONS, delimiter=",")
    population = pd.read_csv(PREPROCESSED_CSP_POPULATION_CSV, delimiter=",")
    population_matrix = pd.read_csv(PREPROCESSED_POPULATION_MATRIX_CSV, delimiter=",")

    csps["lat"] = csps["lat"].astype(str).str.replace(",", ".").astype(float)
    csps["long"] = csps["long"].astype(str).str.replace(",", ".").astype(float)

    valid_cities = {
        row["csp-name"]: (row["lat"], row["long"])
        for _, row in csps.iterrows()
    }

    cities = population_matrix["City"].unique()
    city_locations = {
        city: valid_cities[city]
        for city in cities if city in valid_cities
    }

    fig = plt.figure(figsize=figsize)
    gs = fig.add_gridspec(1, 2, width_ratios=[4, 1])
    ax = fig.add_subplot(gs[0])
    legend_ax = fig.add_subplot(gs[1])
    ax.set_aspect("equal")
    map_plot(ax)

    ax.set_xlim(-8.5, 2.5)
    ax.set_ylim(49.5, 59.5)

    for city, (lon, lat) in city_locations.items():
        pop_row = population.loc[population['Local Authority'] == city, 'Population']
        if not pop_row.empty and SCALE_CSP_NODES_BY_POPULATION_MAP_PLOT:
            city_pop = pop_row.values[0]
            size = city_pop / NODE_SCALING_FACTOR_MAP_PLOT
        else:
            size = 50
        ax.scatter(lon, lat, color="blue", alpha=0.6, s=size)
        if SHOW_CSP_NAMES_MAP_PLOT:
            ax.text(lon, lat, city, fontsize=8, ha='right', va='bottom', alpha=0.7)

    incoming_color = '#FF0000'
    outgoing_color = '#00AA00'

    G = nx.DiGraph()
    for city1, coords1 in city_locations.items():
        for city2, coords2 in city_locations.items():
            if city1 != city2:
                weight = df.loc[city1, city2]
                if weight > min_weight:
                    G.add_edge(city1, city2, weight=weight)

    for city1, city2, data_dict in G.edges(data=True):
        (lon1, lat1) = city_locations[city1]
        (lon2, lat2) = city_locations[city2]

        if df.loc[city2, city2] > df.loc[city1, city1]:
            color = incoming_color
        else:
            color = outgoing_color

        ax.plot(
            [lon1, lon2], [lat1, lat2],
            color=color, alpha=0.5,
            linewidth=data_dict["weight"] / 5000
        )

    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_frame_on(False)

    legend_elements = [
        Line2D([0], [0], color=incoming_color, alpha=0.8, linewidth=3,
               label='Incoming Flow (towards larger cities)'),
        Line2D([0], [0], color=outgoing_color, alpha=0.8, linewidth=3,
               label='Outgoing Flow (towards smaller cities)'),
        plt.scatter([], [], c='blue', alpha=0.8, s=200, label='City')
    ]

    legend_ax.legend(
        handles=legend_elements,
        loc='upper right',
        frameon=True,
        facecolor='white',
        edgecolor='none',
        prop={'family': 'Times New Roman', 'size': 32}
    )
    legend_ax.axis('off')

    plt.tight_layout()
    plt.savefig(f'{output_path}/england_wales_commuting.pdf', dpi=300, bbox_inches='tight', pad_inches=0)
    plt.show()