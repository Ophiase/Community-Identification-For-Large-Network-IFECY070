import networkx as nx
from typing import List, Dict, Tuple


class GirvanNewman:
    @staticmethod
    def _compute_betweenness_centrality(graph: nx.Graph) -> Dict[Tuple[int, int], float]:
        """
        Compute the edge betweenness centrality for all edges in the graph.

        Time Complexity: O(n * m^2)
        - n: number of nodes.
        - m: number of edges.

        Args:
            graph (nx.Graph): The input graph.

        Returns:
            Dict[Tuple[int, int], float]: A dictionary mapping edges to their betweenness centrality values.
        """
        return nx.edge_betweenness_centrality(graph)

    @staticmethod
    def _remove_edge_with_highest_betweenness(graph: nx.Graph) -> Tuple[int, int]:
        """
        Identify and remove the edge with the highest betweenness centrality.

        Time Complexity: O(m log m)
        - m: number of edges.

        Args:
            graph (nx.Graph): The input graph.

        Returns:
            Tuple[int, int]: The removed edge.
        """
        betweenness = GirvanNewman._compute_betweenness_centrality(graph)
        if not betweenness:
            return None
        # Find the edge with the highest betweenness centrality
        edge_to_remove = max(betweenness, key=betweenness.get)
        graph.remove_edge(*edge_to_remove)
        return edge_to_remove

    @staticmethod
    def _get_connected_components(graph: nx.Graph) -> List[set]:
        """
        Get the connected components of the graph.

        Time Complexity: O(n + m)
        - n: number of nodes.
        - m: number of edges.

        Args:
            graph (nx.Graph): The input graph.

        Returns:
            List[set]: A list of sets, where each set represents a connected component.
        """
        return [component for component in nx.connected_components(graph)]

    @staticmethod
    def _modularity(graph: nx.Graph, communities: List[set]) -> float:
        """
        Compute the modularity of the current partition.

        Time Complexity: O(m)
        - m: number of edges.

        Args:
            graph (nx.Graph): The input graph.
            communities (List[set]): A list of sets representing the communities.

        Returns:
            float: The modularity score.
        """
        m = graph.number_of_edges()
        if m == 0:
            return 0.0
        degree = dict(graph.degree())
        Q = 0.0
        for community in communities:
            for i in community:
                for j in community:
                    A_ij = 1 if graph.has_edge(i, j) else 0
                    k_i = degree.get(i, 0)
                    k_j = degree.get(j, 0)
                    Q += A_ij - (k_i * k_j) / (2 * m)
        return Q / (2 * m)

    @staticmethod
    def identification(graph: nx.Graph, max_iterations: int = 100) -> List[set]:
        """
        Perform the Girvan-Newman algorithm to identify communities in the graph.

        Time Complexity: O(n * m^2 * k)
        - n: number of nodes.
        - m: number of edges.
        - k: number of iterations or levels in the hierarchy.

        Args:
            graph (nx.Graph): The input graph.
            max_iterations (int): Maximum number of iterations to perform.

        Returns:
            List[set]: The best partition of the graph into communities.
        """
        original_graph = graph.copy()
        best_modularity = -1.0
        best_partition = []

        for _ in range(max_iterations):
            # Remove the edge with the highest betweenness centrality
            edge_removed = GirvanNewman._remove_edge_with_highest_betweenness(
                graph)
            if edge_removed is None:
                break

            # Get the current connected components
            communities = GirvanNewman._get_connected_components(graph)

            # Compute modularity for the current partition
            current_modularity = GirvanNewman._modularity(
                original_graph, communities)

            # Update the best partition if the current one is better
            if current_modularity > best_modularity:
                best_modularity = current_modularity
                best_partition = communities

        return best_partition
