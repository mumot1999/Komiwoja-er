import copy

from exceptions import VisitedNodeError


class Nodes:
    def __init__(self, size):
        self.nodes = {}
        for i in range(size):
            self.nodes[i] = Node(i)

    def __getitem__(self, item):
        return self.nodes[item]

    def connect(self, node_id_1, node_id_2):
        self.nodes[node_id_1].connect_with_node(self.nodes[node_id_2])
        self.nodes[node_id_2].connect_with_node(self.nodes[node_id_1])

    def get_good_ways(self):
        ways = self.run()
        filtered = []
        for way in ways:
            try:
                new_way = way[:way[1:].index(way[0])+2]
                if len(list(set(new_way))) == len(self.nodes):
                    filtered.append(new_way)
            except:
                pass

        return filtered

    def run(self):
        ways = []
        for start_node in self.nodes.values():
            ways += self.find_ways(start_node)

        return ways

    def find_ways(self, node):
        all_ways = []

        if len(node.neighbors) == 0:
            return [[node.id]]

        for n in node.neighbors:
            nodes_copy = copy.deepcopy(self)
            try:
                nodes_copy[node.id].visit_node(n)
            except VisitedNodeError:
                continue
            ways = nodes_copy.find_ways(nodes_copy[n.id])

            for way in ways:
                all_ways.append([node.id] + way)

        return all_ways


class Node:
    def __init__(self, node_id):
        self.id = node_id
        self.neighbors = []

    def __repr__(self):
        return str({
            'id': self.id,
            'neighbours': list(map(lambda x: x.id, self.neighbors))
        })

    def connect_with_node(self, node):
        if node not in self.neighbors:
            self.neighbors.append(node)

    def visit_node(self, node):
        if node.id not in map(lambda x: x.id, self.neighbors):
            raise VisitedNodeError('Node is not in neighbours')

        for neighbour in self.neighbors:
            if node.id == neighbour.id:
                self.delete_neighbour(node.id)
                neighbour.delete_neighbour(self.id)

    def delete_neighbour(self, node_id):
        for node in self.neighbors:
            if node.id == node_id:
                self.neighbors.remove(node)
