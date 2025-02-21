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

    def test_no_edges_compute_betweenness(self):
        graph = nx.Graph()
        betweenness = GirvanNewman._compute_betweenness(graph)
        self.assertEqual(betweenness, {})

    def test_multiple_highest_betweenness(self):
        graph = nx.cycle_graph(4)  # All edges should have equal betweenness
        initial_edges = set(graph.edges())
        removed_edge = GirvanNewman._remove_highest_betweenness_edge(graph)
        self.assertTrue(removed_edge in initial_edges or tuple(
            reversed(removed_edge)) in initial_edges)
        self.assertEqual(len(graph.edges()), len(initial_edges) - 1)

    def test_modularity_empty_graph(self):
        graph = nx.Graph()
        communities = []
        modularity = GirvanNewman._calculate_modularity(graph, communities)
        self.assertEqual(modularity, 0.0)

    def test_modularity_disconnected_graph(self):
        graph = nx.Graph()
        graph.add_edges_from([(0, 1), (2, 3)])
        communities = [{0, 1}, {2, 3}]
        modularity = GirvanNewman._calculate_modularity(graph, communities)
        # Should be positive for well-separated communities
        self.assertGreater(modularity, 0)

    def test_identification_disconnected_graph(self):
        graph = nx.Graph()
        graph.add_edges_from([(0, 1), (2, 3)])
        partition = GirvanNewman.identification(graph, max_iter=10)
        self.assertEqual(len(partition), 2)
        self.assertTrue({0, 1} in [set(c) for c in partition])
        self.assertTrue({2, 3} in [set(c) for c in partition])

    def test_identification_max_iter_reached(self):
        graph = nx.path_graph(10)  # Long path graph
        partition = GirvanNewman.identification(graph, max_iter=2)
        # Should still return a valid partition
        self.assertTrue(len(partition) > 1)


if __name__ == '__main__':
    unittest.main()
