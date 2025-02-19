import random
import networkx as nx
import unittest
from logic.community_identification.label_propagation import LabelPropagation


class TestLabelPropagation(unittest.TestCase):
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


if __name__ == '__main__':
    unittest.main()
