import pandas as pd
import networkx as nx
import numpy as np
import folium

# Load the data from the CSV file
df = pd.read_csv('NOAA_PLOT.csv')

# Create a graph to represent the roads
city = nx.Graph()

# Add nodes for each data point
for i, row in df.iterrows():
    city.add_node(i, pos=(row['LAT'], row['LONG'], row['NAME']))

# Add edges to connect each node to its neighbors
for i in range(len(df) - 1):
    city.add_edge(i, i + 1, weight=np.sqrt((df.iloc[i]['LAT'] - df.iloc[i+1]['LAT'])**2 + (df.iloc[i]['LONG'] - df.iloc[i+1]['LONG'])**2))

# Calculate the shortest path between each pair of nodes

# Find the indices of the nodes with the given latitude and longitude
source_index = np.where((df['LAT'] == df.iloc[0]['LAT']) & (df['LONG'] == df.iloc[0]['LONG']))[0][0]
target_index = np.where((df['LAT'] == df.iloc[-1]['LAT']) & (df['LONG'] == df.iloc[-1]['LONG']))[0][0]

path = nx.shortest_path(city, source_index, target_index, weight='weight')

# Create a map centered at the average latitude and longitude of the data
mean_lat = df['LAT'].mean()
mean_lon = df['LONG'].mean()

map = folium.Map(location=[mean_lat, mean_lon], zoom_start=13)

# Add markers for each data point
for i, row in df.iterrows():
    folium.Marker([row['LAT'], row['LONG']], tooltip=row['NAME']).add_to(map)

    # # Connect markers with lines along the calculated path
    # if i in path:
    #     next_index = path.index(i) + 1
    #     if next_index < len(path):
    #         next_node = path[next_index]
    #         folium.PolyLine(
    #             [[row['LAT'], row['LONG']], [df.loc[next_node, 'LAT'], df.loc[next_node, 'LONG']]],
    #             color="red", weight=2.5, opacity=1).add_to(map)

# Save the map to an HTML file
map.save('map.html')
