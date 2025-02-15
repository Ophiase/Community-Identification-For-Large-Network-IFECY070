from typing import Dict, Tuple, List
import random
import networkx as nx
from matplotlib import pyplot as plt
from logic.graph_generation import GraphGeneration
from logic.node_partition import NodePartition


class CommunityIdentification:
    @staticmethod
    def _init_partition(graph: nx.Graph) -> Dict[int, int]:
        return {node: node for node in graph.nodes()}

    @staticmethod
    def _compute_degrees(graph: nx.Graph) -> Dict[int, float]:
        return {node: graph.degree(node, weight='weight') for node in graph.nodes()}

    @staticmethod
    def _get_neighboring_communities(graph: nx.Graph, partition: Dict[int, int], node: int) -> Dict[int, float]:
        neighbor_comms: Dict[int, float] = {}
        for neighbor in graph.neighbors(node):
            comm = partition[neighbor]
            weight = graph[node][neighbor].get('weight', 1.0)
            neighbor_comms[comm] = neighbor_comms.get(comm, 0.0) + weight
        return neighbor_comms

    @staticmethod
    def _one_level(graph: nx.Graph, partition: Dict[int, int], resolution: float) -> Tuple[Dict[int, int], bool]:
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
        comm_label: Dict[int, int] = {}
        for label, comm in enumerate(sorted(node_groups.keys())):
            comm_label[comm] = label
        n = graph.number_of_nodes()
        result: List[int] = [0] * n
        for comm, nodes in node_groups.items():
            for node in nodes:
                result[node] = comm_label[comm]
        return result


def display_partition(graph: nx.Graph, name: str, partition_list=None, partition_nodes=None) -> None:
    if partition_list is not None:
        partition_nodes = NodePartition.partition_list_to_partition_nodes(
            partition_list)
    nx.draw(graph, node_color=partition_nodes,
            with_labels=True, cmap=plt.cm.rainbow)
    plt.title(name)


def demo() -> None:
    params = [
        ("Strong Communities", 40, 0.8, 0.1),
        ("Moderate Communities", 40, 0.6, 0.4),
        ("Weak Communities", 40, 0.4, 0.3)
    ]
    rows = len(params)
    plt.figure(figsize=(12, 3 * rows))
    for idx, (name, n_nodes, p, q) in enumerate(params, 1):
        true_partition = NodePartition.partition_list(
            n_nodes, n_partitions=4, as_set=False)
        graph = GraphGeneration.generate_erdos_p_partition_model(
            true_partition, p, q)
        detected_part = CommunityIdentification.louvain(graph, resolution=1.0)
        print(detected_part)
        plt.subplot(rows, 2, 2 * idx - 1)
        display_partition(graph, partition_list=true_partition,
                          name=f"{name} - True Partition")
        plt.subplot(rows, 2, 2 * idx)
        display_partition(graph, partition_nodes=detected_part,
                          name=f"{name} - Louvain Partition")
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    demo()
