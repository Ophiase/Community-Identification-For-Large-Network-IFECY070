import random
import networkx as nx
import unittest
from logic.community_identification.louvain import Louvain


class TestCommunityIdentification(unittest.TestCase):
    def test_init_partition(self):
        graph = nx.path_graph(3)
        partition = Louvain._init_partition(graph)
        self.assertEqual(partition, {0: 0, 1: 1, 2: 2})

    def test_compute_degrees(self):
        graph = nx.Graph()
        graph.add_edge(0, 1)
        degrees = Louvain._compute_degrees(graph)
        self.assertEqual(degrees[0], 1)
        self.assertEqual(degrees[1], 1)

    def test_get_neighboring_communities(self):
        graph = nx.Graph()
        graph.add_edge(0, 1, weight=2)
        partition = {0: 0, 1: 1}
        neighbor_comms = Louvain._get_neighboring_communities(
            graph, partition, 0)
        self.assertEqual(neighbor_comms, {1: 2})

    def test_one_level(self):
        random.seed(42)
        graph = nx.Graph()
        graph.add_edges_from([(0, 1), (1, 2), (2, 0)])
        partition = Louvain._init_partition(graph)
        new_partition, improved = Louvain._one_level(
            graph, partition, resolution=1.0)
        self.assertIsInstance(new_partition, dict)
        self.assertIsInstance(improved, bool)

    def test_aggregate_graph(self):
        graph = nx.Graph()
        graph.add_edge(0, 1, weight=2)
        partition = {0: 0, 1: 0}
        new_graph, mapping = Louvain._aggregate_graph(
            graph, partition)
        self.assertEqual(new_graph.number_of_nodes(), 1)
        edge_data = list(new_graph.edges(data=True))[0][2]
        self.assertEqual(edge_data['weight'], 2)

    def test_louvain_output(self):
        graph = nx.Graph()
        graph.add_edges_from([(0, 1), (1, 2), (2, 0), (2, 3)])
        result = Louvain.identification(graph, resolution=1.0)
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), graph.number_of_nodes())


if __name__ == '__main__':
    unittest.main()
