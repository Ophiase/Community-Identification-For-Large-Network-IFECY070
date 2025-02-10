from typing import Generator, List, Tuple
import networkx as nx
import random
import matplotlib.pyplot as plt
from logic.node_partition import NodePartition
from logic.utils import _cartesian_product, _external_pair


class GraphGeneration:
    @staticmethod
    def erdos_graph_p(n_vertices, probability=None) -> nx.Graph:
        if probability is None:
            probability = 0.5

        g = nx.Graph()
        g.add_nodes_from(range(n_vertices))

        for i in range(n_vertices):
            for j in range(i + 1, n_vertices):
                if random.random() < probability:
                    g.add_edge(i, j)

        return g

    #########################################

    @staticmethod
    def erdos_graph_m(n_vertices, m_edges) -> nx.Graph:
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

    ###################################################################################

    @staticmethod
    def generate_stochastic_block_model(
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

###################################################################################


def main() -> None:
    partition_shuffled = NodePartition.partition_list(50, as_set=False)
    partition_unshuffled = NodePartition.partition_list(
        50, shuffle=False, as_set=False)

    graph_params = [
        ("Erdos-Renyi p", GraphGeneration.erdos_graph_p(10, 0.3), None),
        ("Erdos-Renyi m", GraphGeneration.erdos_graph_m(10, 15), None),
        ("TP3 Graph", GraphGeneration.generate_stochastic_block_model(
            partition_shuffled, p=0.8, q=0.2), partition_shuffled),
        ("TP3 Graph", GraphGeneration.generate_stochastic_block_model(
            partition_unshuffled, p=0.95, q=0.02), partition_unshuffled)
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
