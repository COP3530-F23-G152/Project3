class AdjacencyListGraph:
    def __init__(self, size):
        self.adjacency_list = []
        for _ in range(size):
            self.adjacency_list.append([])

    def add_edge(self, src, dest):
        if len(self.adjacency_list[src]) != 0:
            ret = [i for i, x in enumerate(self.adjacency_list[src]) if x[0] == dest]
            if len(ret) != 0:
                self.adjacency_list[src][ret[0]] = (self.adjacency_list[src][ret[0]][0], self.adjacency_list[src][ret[0]][1]+1)
                return
        
        self.adjacency_list[src].append((dest, 1))

    def count_edges(self, src, dest):
        if len(self.adjacency_list[src]) != 0:
            ret = [x for x in self.adjacency_list[src] if x[0] == dest]
            if len(ret) != 0:
                return ret[0][1]

        return 0 

    def max_in(self, vertex):
        ret = [v[1] for row in self.adjacency_list for v in row if v[0] == vertex]
        if len(ret) == 0:
            return 0
        else:
            return max(ret)
