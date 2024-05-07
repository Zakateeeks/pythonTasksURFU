import unittest
from graph.Graph_Find.search import dijkstra, bell_ford, floyd, a_star
from graph.Graph_Find.create_graph import get_graph


class TestSearchAlgorithms(unittest.TestCase):
    def setUp(self):
        self.vertex = [(0, 1, 5), (1, 2, 3), (2, 0, 2)]
        self.count_vertex = 3
        self.graph = get_graph(self.vertex, self.count_vertex)

    def test_dijkstra(self):
        start_vertex = 0
        expected_result = {0: 0, 1: 5, 2: 8}
        self.assertEqual(dijkstra(self.graph, start_vertex), expected_result)

    def test_bell_ford(self):
        start_vertex = 0
        expected_result = {0: 0, 1: 5, 2: 8}
        self.assertEqual(bell_ford(self.graph, start_vertex), expected_result)

    def test_floyd(self):
        start_vertex = 0
        expected_result = {0: 0, 1: 5, 2: 8}
        self.assertEqual(floyd(self.graph, start_vertex), expected_result)

    def test_a_star(self):
        start_vertex = 0
        expected_result = {0: 0, 1: 5, 2: 8}
        self.assertEqual(a_star(self.graph, start_vertex), expected_result)


if __name__ == '__main__':
    unittest.main()
