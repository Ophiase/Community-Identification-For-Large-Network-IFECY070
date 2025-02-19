from matplotlib import pyplot as plt
from logic.community_identification import CommunityIdentification
from logic.community_identification.girvan_newman import GirvanNewman
from logic.community_identification.label_propagation import LabelPropagation
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

    algorithms = [
        ("Louvain", lambda graph, n_partitions:
            CommunityIdentification.project_partition(
                n_partitions,
                Louvain.identification(graph)
            )
         ),
        ("Label Propagation", lambda graph, n_partitions:
            CommunityIdentification.project_partition(
                n_partitions,
                LabelPropagation.identification(graph)
            )
         ),
        ("Girvan Newman", lambda graph, n_partitions:
            CommunityIdentification.project_partition(
                n_partitions,
                NodePartition.partition_list_to_partition_nodes(
                    GirvanNewman.identification(graph)
                )
            )
         )
        # ("InfoMap", lambda graph:None),
        # ("Fast Greedy", lambda graph:None),
    ]

    n_partitions = 4

    rows = len(params)
    columns = len(algorithms) + 1
    plt.figure(figsize=(4 * columns, 3 * rows))
    for param_idx, (param_name, n_nodes, p, q) in enumerate(params, 0):
        true_partition = NodePartition.partition_list(
            n_nodes, n_partitions=4, as_set=False)
        graph = GraphGeneration.generate_erdos_p_partition_model(
            true_partition, p, q)

        true_labels = NodePartition.partition_list_to_partition_nodes(
            true_partition, n_nodes)
        pos = PartitionVisualization.compute_layout_from_true_partition(
            graph, true_partition)

        plt.subplot(rows, columns, 1 + columns * param_idx)
        PartitionVisualization.display_partition(graph, partition_list=true_partition,
                                                 name=f"{param_name} - True Partition ({p}/{q})", pos=pos)
        print(f"{param_name}")
        for algorithm_idx, (algorithm_name, algorithm) in enumerate(algorithms):
            computed_partition = algorithm(graph, n_partitions)
            error_rate = Metrics.compare_partitions(
                true_labels, computed_partition)

            print(f"\t{algorithm_name} Partition, Error={error_rate:.2f}")
            plt.subplot(rows, columns, columns * param_idx + algorithm_idx + 2)
            PartitionVisualization.display_partition(graph, partition_nodes=computed_partition,
                                                     name=f"{algorithm_name} | error={error_rate:.2f}",
                                                     pos=pos)

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    demo()
