import networkx as nx
from typing import List, Dict, Tuple, Optional, Set


class GirvanNewman:
    @staticmethod
    def _compute_betweenness(graph: nx.Graph) -> Dict[Tuple[int, int], float]:
        """
        Compute edge betweenness centrality.

        Time Complexity: O(n * m^2)
        """
        return nx.edge_betweenness_centrality(graph)

    @staticmethod
    def _remove_highest_betweenness_edge(graph: nx.Graph) -> Optional[Tuple[int, int]]:
        """
        Remove the edge with the highest betweenness centrality.

        Time Complexity: O(m log m)
        """
        betweenness = GirvanNewman._compute_betweenness(graph)
        if not betweenness:
            return None
        edge_to_remove = max(betweenness, key=betweenness.get)
        if graph.has_edge(*edge_to_remove):
            graph.remove_edge(*edge_to_remove)
        return edge_to_remove

    @staticmethod
    def _get_components(graph: nx.Graph) -> List[Set[int]]:
        """
        Retrieve connected components of the graph.

        Time Complexity: O(n + m)
        """
        return list(nx.connected_components(graph))

    @staticmethod
    def _calculate_modularity(original: nx.Graph, communities: List[Set[int]]) -> float:
        """
        Calculate the modularity of a partition.

        Time Complexity: O(m)
        """
        m = original.number_of_edges()
        if m == 0:
            return 0.0
        degree = dict(original.degree())
        Q = 0.0
        for community in communities:
            for i in community:
                for j in community:
                    A = 1 if original.has_edge(i, j) else 0
                    Q += A - (degree[i] * degree[j]) / (2 * m)
        return Q / (2 * m)

    @staticmethod
    def identification(graph: nx.Graph, max_iter: int = 500) -> List[Set[int]]:
        """
        Identify communities using the Girvan-Newman algorithm.

        Time Complexity: O(n * m^2 * k)
        """
        original_graph = graph.copy()
        working_graph = graph.copy()
        best_modularity = -1.0
        best_partition: List[Set[int]] = []

        communities = GirvanNewman._get_components(working_graph)
        modularity = GirvanNewman._calculate_modularity(
            original_graph, communities)
        if modularity > best_modularity:
            best_modularity = modularity
            best_partition = communities

        for _ in range(max_iter):
            edge = GirvanNewman._remove_highest_betweenness_edge(working_graph)
            if edge is None:
                break
            communities = GirvanNewman._get_components(working_graph)
            modularity = GirvanNewman._calculate_modularity(
                original_graph, communities)
            if modularity > best_modularity:
                best_modularity = modularity
                best_partition = communities
            if working_graph.number_of_edges() == 0:
                break
        return best_partition
