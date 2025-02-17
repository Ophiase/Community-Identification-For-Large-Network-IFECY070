from typing import Generator, List, Tuple
import networkx as nx
import random
import matplotlib.pyplot as plt
from logic.node_partition import NodePartition
from logic.utils import _cartesian_product, _external_pair


class GraphGeneration:
    @staticmethod
    def erdos_graph_m(n_vertices: int, m_edges: int) -> nx.Graph:
        if m_edges is None:
            m_edges = n_vertices // 2

        g = nx.Graph()
        g.add_nodes_from(range(n_vertices))

        edges_added = 0
        while edges_added < m_edges:
            u = random.randint(0, n_vertices - 1)
            v = random.randint(0, n_vertices - 1)
            if u != v and not g.has_edge(u, v):
                g.add_edge(u, v)
                edges_added += 1

        return g

    #########################################

    @staticmethod
    def erdos_graph_p(n_vertices: int, probability: float = 0.5) -> nx.Graph:
        g = nx.Graph()
        g.add_nodes_from(range(n_vertices))

        for i in range(n_vertices):
            for j in range(i + 1, n_vertices):
                if random.random() < probability:
                    g.add_edge(i, j)

        return g

    ###################################################################################

    @staticmethod
    def generate_erdos_p_partition_model_bis(
        n_nodes: int, k_partitions: int, p: float, q: float,
        shuffle: bool = True
    ):
        partition = NodePartition.partition_list(
            n_nodes=n_nodes,
            shuffle=shuffle,
            n_partitions=k_partitions,
            as_set=False
        )

        return GraphGeneration.generate_erdos_p_partition_model(partition, p, q)

    @staticmethod
    def generate_erdos_p_partition_model(
        partition: List[List[int]],
        p: float, q: float
    ) -> nx.Graph:
        n_nodes = sum([len(group) for group in partition])

        g = nx.Graph()
        g.add_nodes_from(range(n_nodes))

        # edges with a probability of p
        for group in partition:
            for e1, e2 in _external_pair(len(group)):
                if random.random() < p:
                    g.add_edge(group[e1], group[e2])

        # edges with a probability of q
        for group1, group2 in _external_pair(len(partition)):
            for e1, e2 in _cartesian_product(partition[group1], partition[group2]):
                if random.random() < q:
                    g.add_edge(e1, e2)

        return g

    def generate_erdos_m_partition_model(
        partition: List[List[int]],
        m_edges: float, q: float
    ) -> nx.Graph:
        n_nodes = sum([len(group) for group in partition])

        g = nx.Graph()
        g.add_nodes_from(range(n_nodes))

        # m edges per group
        for group in partition:
            possible_edges = [(u, v) for u in group for v in group if u < v]
            selected_edges = random.sample(
                possible_edges, min(m_edges, len(possible_edges)))
            g.add_edges_from(selected_edges)

        # edges with a probability of q
        for group1, group2 in _external_pair(len(partition)):
            for e1, e2 in _cartesian_product(partition[group1], partition[group2]):
                if random.random() < q:
                    g.add_edge(e1, e2)

        return g

###################################################################################


def main() -> None:
    partition_shuffled = NodePartition.partition_list(50, as_set=False)
    partition_unshuffled = NodePartition.partition_list(
        30, shuffle=False, as_set=False)

    graph_params = [
        ("Erdos-Renyi p", GraphGeneration.erdos_graph_p(10, 0.3), None),
        ("Erdos-Renyi m", GraphGeneration.erdos_graph_m(10, 15), None),

        ("Partitioned Erdos-Renyi p", GraphGeneration.generate_erdos_p_partition_model(
            partition_shuffled, p=0.8, q=0.2), partition_shuffled),
        ("Partitioned Erdos-Renyi p", GraphGeneration.generate_erdos_p_partition_model(
            partition_unshuffled, p=0.95, q=0.02), partition_unshuffled),

        # (
        #     "Partitioned Erdos-Renyi m",
        #     GraphGeneration.generate_erdos_m_partition_model(partition_shuffled, m_edges=10, q=0.2),
        #     partition_shuffled
        # ),
        # (
        #     "Partitioned Erdos-Renyi m",
        #     GraphGeneration.generate_erdos_m_partition_model(partition_unshuffled, m_edges=10, q=0.02),
        #     partition_unshuffled
        # )
    ]

    plt.figure(figsize=(15, 5))
    for i, (title, graph, partition) in enumerate(graph_params, 1):
        plt.subplot(1, 4, i)
        if partition is not None:
            color_map = NodePartition.partition_list_to_partition_nodes(
                partition)
            nx.draw(graph, node_color=color_map,
                    with_labels=True, cmap=plt.cm.rainbow)
        else:
            nx.draw(graph, with_labels=True)
        plt.title(title)
    plt.show()


if __name__ == "__main__":
    main()
