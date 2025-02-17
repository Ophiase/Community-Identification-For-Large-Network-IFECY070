import random
from typing import Dict, List, Tuple
import networkx as nx


class Louvain:
    @staticmethod
    def _init_partition(graph: nx.Graph) -> Dict[int, int]:
        """
        Time Complexity: O(n)
        """
        return {node: node for node in graph.nodes()}

    @staticmethod
    def _compute_degrees(graph: nx.Graph) -> Dict[int, float]:
        """
        Compute the weighted degree for each node.

        Time Complexity: O(n)

        Example:
            Input: graph with edge (0,1) of weight 2
            Output: {0: 2, 1: 2} (if only one edge exists)
        """
        return {node: graph.degree(node, weight='weight') for node in graph.nodes()}

    @staticmethod
    def _get_neighboring_communities(graph: nx.Graph, partition: Dict[int, int], node: int) -> Dict[int, float]:
        """
        Compute the total weight of edges from a given node to each neighboring community.

        Time Complexity: O(d):
        - d: degree of the node (number of neighbors).

        Example:
            Input: node 0 with neighbor 1 in a different community and edge weight 3
            Output: {community_of_1: 3}
        """
        neighbor_comms: Dict[int, float] = {}
        for neighbor in graph.neighbors(node):
            comm = partition[neighbor]
            weight = graph[node][neighbor].get('weight', 1.0)
            neighbor_comms[comm] = neighbor_comms.get(comm, 0.0) + weight
        return neighbor_comms

    @staticmethod
    def _one_level(graph: nx.Graph, partition: Dict[int, int], resolution: float) -> Tuple[Dict[int, int], bool]:
        """
        Perform one level of the Louvain local optimization.
        Iteratively moves nodes to neighboring communities to maximize modularity.

        Time Complexity: O(m * log(n))
        - m: number of edges in the graph.
        - n: number of nodes in the graph.
        - The log(n) factor comes from the need to potentially move each node to a different community.

        Example:
            Input: a triangle graph with initial partition {0:0, 1:1, 2:2}
            Output: (updated partition dict, True) if any improvement was made.
        """
        m = sum(data.get('weight', 1.0)
                for _, _, data in graph.edges(data=True)) / 2.0
        if m == 0:
            return partition, False
        degrees = Louvain._compute_degrees(graph)
        community_total: Dict[int, float] = {}
        for node, comm in partition.items():
            community_total[comm] = community_total.get(
                comm, 0.0) + degrees[node]
        improved = False
        improvement_found = True
        while improvement_found:
            improvement_found = False
            nodes = list(graph.nodes())
            random.shuffle(nodes)
            for node in nodes:
                current_comm = partition[node]
                k_i = degrees[node]
                neighbor_comms = Louvain._get_neighboring_communities(
                    graph, partition, node)
                community_total[current_comm] -= k_i
                best_comm = current_comm
                best_delta = 0.0
                for comm, k_i_in in neighbor_comms.items():
                    delta = k_i_in - resolution * k_i * \
                        community_total.get(comm, 0.0) / (2 * m)
                    if delta > best_delta:
                        best_delta = delta
                        best_comm = comm
                if best_comm != current_comm:
                    partition[node] = best_comm
                    community_total[best_comm] = community_total.get(
                        best_comm, 0.0) + k_i
                    improvement_found = True
                    improved = True
                else:
                    community_total[current_comm] += k_i
        return partition, improved

    @staticmethod
    def _aggregate_graph(graph: nx.Graph, partition: Dict[int, int]) -> Tuple[nx.Graph, Dict[int, int]]:
        """
        Aggregate the graph based on current partition.
        Each community is merged into a single node, and edge weights between communities are summed.

        Time Complexity: O(m)
        - m: number of edges in the graph.

        Example:
            Input: graph with edge between nodes in the same community.
            Output: new_graph with one node representing that community.
        """
        new_graph = nx.Graph()
        for u, v, data in graph.edges(data=True):
            comm_u = partition[u]
            comm_v = partition[v]
            weight = data.get('weight', 1.0)
            if new_graph.has_edge(comm_u, comm_v):
                new_graph[comm_u][comm_v]['weight'] += weight
            else:
                new_graph.add_edge(comm_u, comm_v, weight=weight)
        communities = set(partition.values())
        new_graph.add_nodes_from(communities)
        mapping = {comm: idx for idx, comm in enumerate(sorted(communities))}
        return new_graph, mapping

    @staticmethod
    def louvain(graph: nx.Graph, resolution: float = 1.0) -> List[int]:
        """
        Perform the Louvain algorithm on the graph and return a list where the i-th element is the community
        label for node i.

        Time Complexity: O(m * log(n))
        - m: number of edges in the graph.
        - n: number of nodes in the graph.
        - The log(n) factor comes from the iterative process of moving nodes and aggregating the graph.

        Example:
            Input: graph with 5 nodes, some edges.
            Output: [0, 0, 1, 1, 0] where each index corresponds to a node.
        """
        node_groups: Dict[int, List[int]] = {
            node: [node] for node in graph.nodes()}
        current_graph = graph.copy()
        current_partition = Louvain._init_partition(
            current_graph)
        while True:
            current_partition, improved = Louvain._one_level(
                current_graph, current_partition, resolution)
            if not improved:
                break
            new_graph, mapping = Louvain._aggregate_graph(
                current_graph, current_partition)
            new_node_groups: Dict[int, List[int]] = {}
            for node in current_graph.nodes():
                comm = current_partition[node]
                new_comm = mapping[comm]
                if new_comm not in new_node_groups:
                    new_node_groups[new_comm] = []
                new_node_groups[new_comm].extend(node_groups[node])
            node_groups = new_node_groups
            current_graph = new_graph
            current_partition = Louvain._init_partition(
                current_graph)
        comm_label: Dict[int, int] = {
            comm: label for label, comm in enumerate(sorted(node_groups.keys()))}
        n = graph.number_of_nodes()
        result: List[int] = [0] * n
        for comm, nodes in node_groups.items():
            for node in nodes:
                result[node] = comm_label[comm]
        return result
