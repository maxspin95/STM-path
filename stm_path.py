import numpy as np
import pandas as pd

class Graph:
    def __init__(self):
       self.nodes = []     #metro stations
       self.edges = {}     #connections between stations
       self.colors = []    #colours of the stations

    #you can add a metro station in the graph
    def add_node(self, v):
       self.nodes.append(v)
    
    #you can add a color to a station (and should)
    def add_color(self, v, c):
       self.colors.append((v, c[0].split("/")))
    
    #you can (and should) add a distance (in minutes) between stations
    def add_edge(self, v1, v2, dist):
       self.edges[v1, v2] = dist

    # neighbours of a station
    def get_neighbours(self, u):
       neighbours = []
       for k, e in self.edges.items():
           if ((u in k) and (u == k[0])):
              neighbours.append(k[1])
           elif ((u in k) and (u == k[1])):
              neighbours.append(k[0])
       return neighbours

    # distance between station
    def get_distance(self, u, v):
       for k, e in self.edges.items():
           if (u in k and v in k):
              return self.edges[k]
       return None

#closest station
def min_distance(dist, q):
    min_index = None
    min_value = float("inf")
    for v in q:
       if (dist[v] < min_value):
           min_value = dist[v]
           min_index = v
    return min_index

#color of a given station
def get_color(graph, v):
    color = None
    for u in graph.colors:
       if v == u[0]:
           color = u[1]
    return color


def dijkstra(graph, source, end):
    #initialization
    dist = {}
    prev = {}
    all_stations = [source]
    temp_color = get_color(graph, source)

    for v in graph.nodes:
       dist[v] = float("inf")
       prev[v] = None
    q = set(graph.nodes)

    #distance to the source is 0
    dist[source] = 0

    while (len(q) > 0):
       #select the closest station
       u = min_distance(dist, q)
       all_stations.append(u)
       #remove it from the searching list
       q.remove(u)

       #we search the neighbours
       for v in graph.get_neighbours(u):
           if ((prev != {}) and (list(set(get_color(graph, u)) & set(get_color(graph, v))) == [])):
              temp_color = get_color(graph, u)
              alt = dist[u] + graph.get_distance(u, v)+5
           else:
              alt = dist[u] + graph.get_distance(u, v)
           if alt < dist[v]:
              dist[v] = alt
              prev[v] = u

    return dist, prev, all_stations


#import information about the network
stations = pd.read_csv('stations_STM.csv')       #nodes (stations)
connects = pd.read_csv('connect_STM.csv')        #edges (connections)

#we create the metro of Montreal
graph = Graph()

for s in stations["Stations"]:
    graph.add_node(s)

for k in range(len(stations["Stations"])):
    graph.add_color(stations["Stations"][k], [stations["Colours"][k]])

for k in range(len(connects["distance"])):
    graph.add_edge(connects["Station_start"][k],
                   connects["Station_end"][k], connects["distance"][k])

#the user input informations about their travel
start_station = input("What station are you in? ")
while start_station not in graph.nodes:
    print("This is not a valid station. ")
    start_station = input("What station are you in? ")

exit_station = input("Where do you need to go? ")
while exit_station not in graph.nodes:
    print("This is not a valid station. ")
    exit_station = input("Where do you need to go? ")

#we want the path taken
def path(start, end, prev):
    path = [end]
    temp = end
    path.append(prev.get(temp))
    while temp != start:
       temp = prev.get(temp)
       path.append(prev.get(temp))
    path.pop()
    path = path[::-1]
    return path

#computing the path to take and printing it
dist, prev, stations = dijkstra(graph, start_station, exit_station)
print(path(start_station, exit_station, prev))