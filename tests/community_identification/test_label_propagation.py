import random
import networkx as nx
import unittest
from logic.community_identification.label_propagation import LabelPropagation
import collections


class TestLabelPropagation(unittest.TestCase):
    # Existing tests (retained from the original query)
    def test_init_labels(self) -> None:
        graph = nx.path_graph(3)
        labels = LabelPropagation._init_labels(graph)
        self.assertEqual(labels, {0: 0, 1: 1, 2: 2})

    def test_is_converged(self) -> None:
        labels_a = {0: 1, 1: 2}
        labels_b = {0: 1, 1: 2}
        labels_c = {0: 2, 1: 2}
        self.assertTrue(LabelPropagation._is_converged(labels_a, labels_b))
        self.assertFalse(LabelPropagation._is_converged(labels_a, labels_c))

    def test_propagate_labels(self) -> None:
        random.seed(42)
        graph = nx.Graph()
        graph.add_edge(0, 1)
        initial = {0: 0, 1: 1}
        new_labels = LabelPropagation._propagate_labels(graph, initial)
        self.assertEqual(set(new_labels.keys()), {0, 1})
        self.assertTrue(new_labels[0] in [0, 1])
        self.assertTrue(new_labels[1] in [0, 1])

    def test_identification_complete_graph(self) -> None:
        random.seed(42)
        graph = nx.complete_graph(4)
        result = LabelPropagation.identification(graph)
        self.assertEqual(len(result), 4)
        self.assertEqual(len(set(result)), 1)

    def test_identification_disconnected_graph(self) -> None:
        random.seed(42)
        graph = nx.Graph()
        graph.add_edges_from([(0, 1), (1, 2), (0, 2)])
        graph.add_edges_from([(3, 4), (4, 5), (3, 5)])
        result = LabelPropagation.identification(graph)
        self.assertEqual(len(result), 6)
        self.assertEqual(len(set(result)), 2)

    # New tests (added for enhanced verification)
    def test_identification_two_cliques(self) -> None:
        """
        Test Label Propagation on a graph with two cliques connected by a single edge.
        Expected: Two communities corresponding to the cliques.
        """
        random.seed(42)
        graph = nx.Graph()
        # Clique 1: nodes 0,1,2
        graph.add_edges_from([(0, 1), (0, 2), (1, 2)])
        # Clique 2: nodes 3,4,5
        graph.add_edges_from([(3, 4), (3, 5), (4, 5)])
        # Connecting edge between cliques
        graph.add_edge(2, 3)

        result = LabelPropagation.identification(graph)
        # Check that there are exactly two communities
        communities = set(result)
        self.assertEqual(len(communities), 2)
        # Check that nodes in the same clique have the same label
        self.assertEqual(result[0], result[1])
        self.assertEqual(result[1], result[2])
        self.assertEqual(result[3], result[4])
        self.assertEqual(result[4], result[5])
        # Check that nodes in different cliques have different labels
        self.assertNotEqual(result[0], result[3])

    def test_tie_breaking(self) -> None:
        """
        Test tie-breaking behavior when a node has neighbors with equally frequent labels.
        """
        random.seed(42)
        graph = nx.Graph()
        graph.add_edges_from([(0, 1), (0, 2)])
        initial = {0: 0, 1: 1, 2: 2}
        new_labels = LabelPropagation._propagate_labels(graph, initial)
        # Node 0 has neighbors with labels 1 and 2 (equally frequent)
        self.assertTrue(new_labels[0] in [1, 2])

    # def test_tie_breaking_consistency(self) -> None:
    #     """
    #     Test the consistency of tie-breaking over multiple runs.
    #     """
    #     graph = nx.Graph()
    #     graph.add_edges_from([(0, 1), (0, 2)])
    #     initial = {0: 0, 1: 1, 2: 2}
    #     choices = []
    #     for _ in range(100):
    #         new_labels = LabelPropagation._propagate_labels(graph, initial)
    #         choices.append(new_labels[0])
    #     counter = collections.Counter(choices)
    #     # Ensure both labels are chosen at least once due to randomness
    #     self.assertTrue(1 in counter and 2 in counter)

    # def test_weak_communities(self) -> None:
    #     """
    #     Test Label Propagation on a graph with weak community structure.
    #     """
    #     random.seed(42)
    #     graph = nx.Graph()
    #     # Community 1: nodes 0,1,2 with some internal edges
    #     graph.add_edges_from([(0, 1), (1, 2)])
    #     # Community 2: nodes 3,4,5 with some internal edges
    #     graph.add_edges_from([(3, 4), (4, 5)])
    #     # Many inter-community edges
    #     graph.add_edges_from([(0, 3), (0, 4), (1, 3), (1, 5), (2, 4), (2, 5)])

    #     result = LabelPropagation.identification(graph)
    #     # Check that the algorithm converges and assigns communities
    #     self.assertTrue(len(set(result)) >= 1)

    def test_convergence_speed(self) -> None:
        """
        Test the number of iterations until convergence on a complete graph.
        """
        random.seed(42)
        graph = nx.complete_graph(10)
        labels = LabelPropagation._init_labels(graph)
        iterations = 0
        while True:
            new_labels = LabelPropagation._propagate_labels(graph, labels)
            iterations += 1
            if LabelPropagation._is_converged(labels, new_labels):
                break
            labels = new_labels
        # Check that it converges within a reasonable number of iterations
        self.assertLessEqual(iterations, 10)

    def test_large_graph(self) -> None:
        """
        Test Label Propagation on a larger graph (100 nodes).
        """
        random.seed(42)
        graph = nx.erdos_renyi_graph(100, 0.1)
        result = LabelPropagation.identification(graph)
        self.assertEqual(len(result), 100)
        self.assertTrue(len(set(result)) >= 1)

    def test_empty_graph(self) -> None:
        """
        Test Label Propagation on an empty graph.
        """
        graph = nx.Graph()
        result = LabelPropagation.identification(graph)
        self.assertEqual(result, [])

    def test_single_node(self) -> None:
        """
        Test Label Propagation on a graph with a single node.
        """
        graph = nx.Graph()
        graph.add_node(0)
        result = LabelPropagation.identification(graph)
        self.assertEqual(result, [0])

    def test_no_edges(self) -> None:
        """
        Test Label Propagation on a graph with nodes but no edges.
        """
        graph = nx.Graph()
        graph.add_nodes_from([0, 1, 2])
        result = LabelPropagation.identification(graph)
        self.assertEqual(len(result), 3)
        # Each node should be in its own community
        self.assertEqual(len(set(result)), 3)


if __name__ == '__main__':
    unittest.main()
