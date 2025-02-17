
from matplotlib import pyplot as plt
from logic.graph_generation import GraphGeneration
from logic.node_partition import NodePartition
import networkx as nx


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
