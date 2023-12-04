class AdjacencyMatrixGraph:
    def __init__(self, size):
        self.adjacency_list = []
        for _ in range(size):
            self.adjacency_list.append([0] * size)

    def add_edge(self, src, dest):
        self.adjacency_list[src][dest] += 1 

    def count_edges(self, src, dest):
        return self.adjacency_list[src][dest]

    def max_in(self, vertex):
        return max(self.adjacency_list[src][vertex] for src in range(len(self.adjacency_list)))

    def total_in(self, vertex):
        return sum(self.adjacency_list[src][vertex] for src in range(len(self.adjacency_list)))
