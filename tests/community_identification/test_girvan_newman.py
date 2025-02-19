import unittest
import networkx as nx
from typing import Set, List
from logic.community_identification.girvan_newman import GirvanNewman


class TestGirvanNewman(unittest.TestCase):
    def test_compute_betweenness(self) -> None:
        graph = nx.path_graph(3)
        betweenness = GirvanNewman._compute_betweenness(graph)
        self.assertIsInstance(betweenness, dict)
        self.assertTrue(any(edge in betweenness for edge in [(0, 1), (1, 0)]))
        self.assertTrue(any(edge in betweenness for edge in [(1, 2), (2, 1)]))

    def test_remove_highest_betweenness_edge(self) -> None:
        graph = nx.path_graph(3)
        initial_edges = set(graph.edges())
        removed_edge = GirvanNewman._remove_highest_betweenness_edge(graph)
        self.assertEqual(len(graph.edges()), len(initial_edges) - 1)
        self.assertFalse(removed_edge in graph.edges() or tuple(
            reversed(removed_edge)) in graph.edges())

    def test_get_components(self) -> None:
        graph = nx.Graph()
        graph.add_edges_from([(0, 1), (2, 3)])
        components = GirvanNewman._get_components(graph)
        self.assertEqual(len(components), 2)
        self.assertTrue({0, 1} in components)
        self.assertTrue({2, 3} in components)

    def test_calculate_modularity(self) -> None:
        graph = nx.Graph()
        graph.add_edges_from([(0, 1), (1, 2), (2, 0)])
        communities: List[Set[int]] = [set([0, 1, 2])]
        modularity = GirvanNewman._calculate_modularity(graph, communities)
        self.assertIsInstance(modularity, float)

    def test_identification(self) -> None:
        graph = nx.Graph()
        graph.add_edges_from([(0, 1), (1, 2), (2, 0)])
        graph.add_edges_from([(3, 4), (4, 5), (5, 3)])
        graph.add_edge(2, 3)
        partition = GirvanNewman.identification(graph, max_iter=10)
        self.assertEqual(len(partition), 2)
        communities = [set(c) for c in partition]
        self.assertTrue(any({0, 1, 2}.issubset(comm) for comm in communities))
        self.assertTrue(any({3, 4, 5}.issubset(comm) for comm in communities))


if __name__ == '__main__':
    unittest.main()
