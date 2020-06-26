class Vertex:
    def __init__(self, location):
        self.location = location
        self.adjacency_list = []

    def vertex_string(self):
        return self.location


class Graph:
    def __init__(self):
        self.adjacency_list = {}
        self.edge_weights = {}

    def add_vertex(self, new_vertex):
        self.adjacency_list[new_vertex] = []

    def add_edge(self, vertex1, vertex2, weight=1.0):
        self.edge_weights[(vertex1, vertex2)] = weight
        self.adjacency_list[vertex1].append(vertex2)
        self.edge_weights[(vertex2, vertex1)] = weight
        self.adjacency_list[vertex2].append(vertex1)

    def get_vertex(self, locale):

        for vertex in self.adjacency_list:
            if vertex.location == locale:
                return vertex
        return None

    def get_distance_by_address(self, address_a, address_b):
        vertex_a = self.get_vertex(address_a)
        vertex_b = self.get_vertex(address_b)

        return self.edge_weights[(vertex_a, vertex_b)]

    def get_weight(self, vertex_a, vertex_b):
        return self.edge_weights[(vertex_a, vertex_b)]
