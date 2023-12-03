import pandas as pd

class AdjacencyListGraph:
    def __init__(self):
        self.adjacency_list = {}

    def add_vertex(self, vertex):
        if vertex not in self.adjacency_list:
            self.adjacency_list[vertex] = {'name': vertex, 'incoming_edges': 0}

    def add_edge(self, source, target, weight=1):
        if source in self.adjacency_list and target in self.adjacency_list:
            if target in self.adjacency_list[source]:
                # Edge already exists, increase the weight
                self.adjacency_list[source][target] += weight
            else:
                # Edge doesn't exist, add a new edge
                self.adjacency_list[source][target] = weight
                self.adjacency_list[target]['incoming_edges'] += 1

    def display_adjacency_list(self):
        adjacency_list_df = pd.DataFrame(columns=['Zone','weight'])
        for vertex, data in self.adjacency_list.items():
            for neighbor, weight in self.adjacency_list[vertex].items():
                if neighbor != 'name' and neighbor != 'incoming_edges':
                    neighbor_name = self.adjacency_list[neighbor]['name']
                    print(f"{neighbor_name}, {weight} times")
            print(f"{data['name']} has {data['incoming_edges']} incoming rides.")
            print()
            
    def display_adjacency_list_for_vertex(self, vertex_name):
        if vertex_name in self.adjacency_list:
            data = self.adjacency_list[vertex_name]
            adjacency_list_df = pd.DataFrame(columns=['Zone','Weight'])
            for neighbor, weight in data.items():
                if (neighbor != 'name' and neighbor != 'incoming_edges'):
                    if ((self.adjacency_list[neighbor]['name'] != 264) and (self.adjacency_list[neighbor]['name'] != 265)):
                        neighbor_name = self.adjacency_list[neighbor]['name']
                        adjacency_list_df.loc[len(adjacency_list_df.index)] = [self.adjacency_list[neighbor]['name'], weight]
            adjacency_list_df = adjacency_list_df.sort_values(by='Weight', ascending = False)
            color_scale = 255/len(adjacency_list_df)
            colors = list([])
            for i in range(len(adjacency_list_df)):
                colors.append(int(255 - (i * color_scale)))
            adjacency_list_df['Red_Value'] = colors
            return(adjacency_list_df)
        else:
            print(f"Vertex with name {vertex_name} not found in the graph.")
            return(adjacency_list_df)
