class AdjacencyListGraph:
    def __init__(self, size):
        self.adjacency_list = []
        for _ in range(size):
            self.adjacency_list.append([])

    def add_edge(self, src, dest):
        if not self.adjacency_list[src].empty():
            ret = [x for x in self.adjacency_list if x[0] == dest]
            if not ret.empty():
                ret[0] += 1
                return
        
        self.adjacency_list.append((dest, 1))

    def count_edges(self, src, dest):
        if not self.adjacency_list[src].empty():
            ret = [x for x in self.adjacency_list if x[0] == dest]
            if not ret.empty():
                return ret[0]

        return 0 

    def max_in(self, vertex):
        return max(v[1] for row in self.adjacency_list for v in row if v[0] == vertex)
