from matplotlib import pyplot as plt
from logic.community_identification import CommunityIdentification
from logic.community_identification.louvain import Louvain
from logic.graph_generation import GraphGeneration
from logic.metrics import Metrics
from logic.node_partition import NodePartition
from visualization.partition_visualization import PartitionVisualization


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
        detected_part = Louvain.identification(graph, resolution=1.0)
        detected_part = CommunityIdentification.project_partition(
            n_partitions, detected_part)

        true_labels = NodePartition.partition_list_to_partition_nodes(
            true_partition, n_nodes)
        error_rate = Metrics.compare_partitions(true_labels, detected_part)
        pos = PartitionVisualization.compute_layout_from_true_partition(
            graph, true_partition)

        print(f"{name} error rate: {error_rate:.2f}")

        plt.subplot(rows, 2, 2 * idx - 1)
        PartitionVisualization.display_partition(graph, partition_list=true_partition,
                                                 name=f"{name} - True Partition ({p}/{q})", pos=pos)
        plt.subplot(rows, 2, 2 * idx)
        PartitionVisualization.display_partition(graph, partition_nodes=detected_part,
                                                 name=f"{name} - Louvain Partition, error={error_rate:.2f}",
                                                 pos=pos)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    demo()
