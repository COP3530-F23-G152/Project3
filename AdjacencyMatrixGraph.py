class AdjacencyMatrixGraph:
    def __init__(self, size):
        self.adjacency_matrix = []
        for _ in range(size):
            self.adjacency_matrix.append([0] * size)

    # Adds one edge to the graph
    def add_edge(self, src, dest):
        self.adjacency_matrix[src][dest] += 1 

    # Counts the number of edges going from node src to node dest
    def count_edges(self, src, dest):
        return self.adjacency_matrix[src][dest]

    # Find the maximum number of edges from node v going to node vertex where v is any node
    def max_in(self, vertex):
        return max(self.adjacency_matrix[src][vertex] for src in range(len(self.adjacency_matrix)))

    # Find the sum of the edges going to node vertex 
    def total_in(self, vertex):
        return sum(self.adjacency_matrix[src][vertex] for src in range(len(self.adjacency_matrix)))
