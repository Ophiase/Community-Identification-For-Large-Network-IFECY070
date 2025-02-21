import random
from typing import Dict, List
import networkx as nx
import collections


class LabelPropagation:
    @staticmethod
    def _init_labels(graph: nx.Graph) -> Dict[int, int]:
        """
        Initialize each node with a unique label.

        Time Complexity: O(n)
        - n: number of nodes in the graph.
        """
        return {node: node for node in graph.nodes()}

    @staticmethod
    def _propagate_labels(graph: nx.Graph, labels: Dict[int, int]) -> Dict[int, int]:
        """
        Update the labels of each node based on the labels of its neighbors.

        Time Complexity: O(m)
        - m: number of edges in the graph. For each node, we process its neighbors,
          and the total number of neighbor lookups across all nodes is proportional
          to the number of edges.
        """
        new_labels = labels.copy()
        nodes = list(graph.nodes())
        random.shuffle(nodes)
        for node in nodes:
            neighbor_labels = [new_labels[neighbor]
                               for neighbor in graph.neighbors(node)]
            if neighbor_labels:
                label_counts = collections.Counter(neighbor_labels)
                max_count = max(label_counts.values())
                max_labels = [label for label,
                              count in label_counts.items() if count == max_count]
                new_label = random.choice(max_labels)
                new_labels[node] = new_label
        return new_labels

    @staticmethod
    def _is_converged(old_labels: Dict[int, int], new_labels: Dict[int, int]) -> bool:
        """
        Check if the labels have converged (no changes).

        Time Complexity: O(n)
        - n: number of nodes in the graph. Compares the labels of all nodes between
          two dictionaries.
        """
        return old_labels == new_labels

    @staticmethod
    def identification(graph: nx.Graph, max_iter: int = 100) -> List[int]:
        """
        Perform the Label Propagation Algorithm on the graph and return a list where
        the i-th element is the community label for node i.

        Time Complexity: O(m * k)
        - m: number of edges in the graph.
        - k: number of iterations until convergence, capped at max_iter. Each iteration
          involves O(m) work in _propagate_labels, and the loop runs up to k times.
        """
        labels = LabelPropagation._init_labels(graph)
        for _ in range(max_iter):
            new_labels = LabelPropagation._propagate_labels(graph, labels)
            if LabelPropagation._is_converged(labels, new_labels):
                break
            labels = new_labels
        n = graph.number_of_nodes()
        result = [0] * n
        unique_labels = sorted(set(labels.values()))
        label_map = {label: idx for idx, label in enumerate(unique_labels)}
        for node, label in labels.items():
            result[node] = label_map[label]
        return result
