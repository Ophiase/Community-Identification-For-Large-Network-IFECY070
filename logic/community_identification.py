from typing import Dict, Tuple, List
import random
import math
import networkx as nx
import numpy as np
from scipy.optimize import linear_sum_assignment
from matplotlib import pyplot as plt
from logic.graph_generation import GraphGeneration
from logic.node_partition import NodePartition


class CommunityIdentification:
    @staticmethod
    def _init_partition(graph: nx.Graph) -> Dict[int, int]:
        return {node: node for node in graph.nodes()}

    @staticmethod
    def _compute_degrees(graph: nx.Graph) -> Dict[int, float]:
        """
        Compute the weighted degree for each node.

        Example:
            Input: graph with edge (0,1) of weight 2
            Output: {0: 2, 1: 2} (if only one edge exists)
        """
        return {node: graph.degree(node, weight='weight') for node in graph.nodes()}

    @staticmethod
    def _get_neighboring_communities(graph: nx.Graph, partition: Dict[int, int], node: int) -> Dict[int, float]:
        """
        Compute the total weight of edges from a given node to each neighboring community.

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

        Example:
            Input: a triangle graph with initial partition {0:0, 1:1, 2:2}
            Output: (updated partition dict, True) if any improvement was made.
        """
        m = sum(data.get('weight', 1.0)
                for _, _, data in graph.edges(data=True)) / 2.0
        if m == 0:
            return partition, False
        degrees = CommunityIdentification._compute_degrees(graph)
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
                neighbor_comms = CommunityIdentification._get_neighboring_communities(
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

        Example:
            Input: graph with 5 nodes, some edges.
            Output: [0, 0, 1, 1, 0] where each index corresponds to a node.
        """
        node_groups: Dict[int, List[int]] = {
            node: [node] for node in graph.nodes()}
        current_graph = graph.copy()
        current_partition = CommunityIdentification._init_partition(
            current_graph)
        while True:
            current_partition, improved = CommunityIdentification._one_level(
                current_graph, current_partition, resolution)
            if not improved:
                break
            new_graph, mapping = CommunityIdentification._aggregate_graph(
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
            current_partition = CommunityIdentification._init_partition(
                current_graph)
        comm_label: Dict[int, int] = {
            comm: label for label, comm in enumerate(sorted(node_groups.keys()))}
        n = graph.number_of_nodes()
        result: List[int] = [0] * n
        for comm, nodes in node_groups.items():
            for node in nodes:
                result[node] = comm_label[comm]
        return result

    @staticmethod
    def project_partition(
        target_groups: int,
        detected_partition: List[int]
    ) -> List[int]:
        """
        Project the detected partition to a specified number of groups by merging groups.
        The merging is done by sorting the unique detected groups and mapping them proportionally 
        to new labels ranging from 0 to target_groups - 1.

        Example:
            Input: target_groups = 3, detected_partition = [0, 1, 2, 3, 4]
            Suppose unique groups sorted are [0, 1, 2, 3, 4] (total 5 groups). Then:
              mapping: 0 -> int(0*3/5)=0,
                       1 -> int(1*3/5)=0,
                       2 -> int(2*3/5)=1,
                       3 -> int(3*3/5)=1,
                       4 -> int(4*3/5)=2.
            Output: [0, 0, 1, 1, 2]
        """
        unique = sorted(set(detected_partition))
        k = len(unique)
        mapping = {group: int(index * target_groups / k)
                   for index, group in enumerate(unique)}
        return [mapping[label] for label in detected_partition]


def compare_partitions(true_labels: List[int], detected_labels: List[int]) -> float:
    """
    Compare two partitions and return the error rate (fraction of nodes misclassified).
    Uses the Hungarian algorithm for optimal matching between community labels.

    Example:
        Input: true_labels = [0, 0, 1, 1], detected_labels = [1, 1, 0, 0]
        Output: 0.0 (all nodes correctly classified after label matching)
    """
    unique_true = sorted(set(true_labels))
    unique_detected = sorted(set(detected_labels))
    cost_matrix = np.zeros((len(unique_true), len(unique_detected)), dtype=int)
    for i in range(len(true_labels)):
        cost_matrix[true_labels[i]][detected_labels[i]] += 1
    row_ind, col_ind = linear_sum_assignment(-cost_matrix)
    correct = cost_matrix[row_ind, col_ind].sum()
    error_rate = 1 - correct / len(true_labels)
    return error_rate


def partition_list_to_labels(partition_list: List[List[int]], n: int) -> List[int]:
    """
    Convert a partition list (list of communities, each a list of node indices) into a label list.

    Example:
        Input: partition_list = [[0, 1, 2], [3, 4]], n = 5
        Output: [0, 0, 0, 1, 1]
    """
    labels = [0] * n
    for label, community in enumerate(partition_list):
        for node in community:
            labels[node] = label
    return labels


def compute_layout_from_true_partition(graph: nx.Graph, partition_list: List[List[int]]) -> Dict[int, Tuple[float, float]]:
    """
    Compute a layout for the graph where each community is assigned a position on a large circle.
    Within each community, nodes are positioned randomly on a small subcircle around the community center.

    Example:
        Input: partition_list = [[0, 1, 2], [3, 4]]
        Output: {0: (x0, y0), 1: (x1, y1), ..., 4: (x4, y4)} where positions reflect community structure.
    """
    pos: Dict[int, Tuple[float, float]] = {}
    num_groups = len(partition_list)
    big_radius = 10.0
    small_radius = 6.0
    for i, community in enumerate(partition_list):
        angle = 2 * math.pi * i / num_groups
        center_x = big_radius * math.cos(angle)
        center_y = big_radius * math.sin(angle)
        for node in community:
            theta = random.uniform(0, 2 * math.pi)
            r = random.uniform(0, small_radius)
            pos[node] = (center_x + r * math.cos(theta),
                         center_y + r * math.sin(theta))
    return pos


def display_partition(graph: nx.Graph, name: str, partition_list=None, partition_nodes=None, pos=None) -> None:
    """
    Display the graph using a given partition.

    Example:
        Input: a graph and partition_list = [[0,1,2],[3,4]]
        Behavior: displays the graph colored by communities.
    """
    if partition_list is not None:
        partition_nodes = NodePartition.partition_list_to_partition_nodes(
            partition_list)
    nx.draw(graph, pos=pos, node_color=partition_nodes,
            with_labels=True, cmap=plt.cm.rainbow)
    plt.title(name)


def demo() -> None:
    """
    Run a demo with three synthetic graphs and display the true vs detected partitions.
    Also computes and prints the error rate of the detected partition compared to the true partition.

    Example:
        Behavior: generates graphs with "Strong", "Moderate", and "Weak" communities and plots their layouts.
    """
    params = [
        ("Strong Communities", 50, 0.8, 0.1),
        ("Moderate Communities", 50, 0.7, 0.2),
        ("Weak Communities", 50, 0.5, 0.3)
    ]
    n_partitions = 4

    rows = len(params)
    plt.figure(figsize=(12, 3 * rows))
    for idx, (name, n_nodes, p, q) in enumerate(params, 1):
        true_partition = NodePartition.partition_list(
            n_nodes, n_partitions=4, as_set=False)
        graph = GraphGeneration.generate_erdos_p_partition_model(
            true_partition, p, q)
        detected_part = CommunityIdentification.louvain(graph, resolution=1.0)
        detected_part = CommunityIdentification.project_partition(
            n_partitions, detected_part)

        true_labels = partition_list_to_labels(true_partition, n_nodes)
        error_rate = compare_partitions(true_labels, detected_part)
        pos = compute_layout_from_true_partition(graph, true_partition)

        print(f"{name} error rate: {error_rate:.2f}")

        plt.subplot(rows, 2, 2 * idx - 1)
        display_partition(graph, partition_list=true_partition,
                          name=f"{name} - True Partition ({p}/{q})", pos=pos)
        plt.subplot(rows, 2, 2 * idx)
        display_partition(graph, partition_nodes=detected_part,
                          name=f"{name} - Louvain Partition, error={error_rate:.2f}",
                          pos=pos)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    demo()
