from logic.community_identification.base import CommunityIdentification
from logic.community_identification.louvain import Louvain
from logic.graph_generation import GraphGeneration
from logic.metrics import Metrics
from logic.node_partition import NodePartition
from visualization.partition_visualization import PartitionVisualization
import time


def main() -> None:
    params = [
        ("Strong Communities", 1000, 0.8, 0.1),
        ("Moderate Communities", 1000, 0.7, 0.2),
        ("Weak Communities", 1000, 0.5, 0.3)
    ]

    algorithms = [
        ("Louvain", lambda graph, n_partitions:
            CommunityIdentification.project_partition(
                n_partitions,
                Louvain.identification(graph, resolution=1.0)
            )
         ),
        # ("Girvan Newman", lambda graph:None),
        # ("Label Propagation", lambda graph:None),
        # ("InfoMap", lambda graph:None),
        # ("Fast Greedy", lambda graph:None),
    ]

    n_partitions = 4

    #########################################

    for param_name, n_nodes, p, q in params:
        print(f"{param_name}")

        _start_time = time.time()
        true_partition = NodePartition.partition_list(
        n_nodes, n_partitions=4, as_set=False)
        _elapsed_time_0 = time.time() - _start_time
        graph = GraphGeneration.generate_erdos_p_partition_model(
            true_partition, p, q)
        _elapsed_time_1 = time.time() - _start_time - _elapsed_time_0
        true_labels = NodePartition.partition_list_to_partition_nodes(
            true_partition, n_nodes)

        print(f"\tPartition ({n_partitions}) Generation Time\t= {_elapsed_time_0:.4f}") 
        print(f"\tGraph Generation Time\t\t= {_elapsed_time_1:.4f}")

        for algorithm_name, algorithm in algorithms:
            _start_time = time.time()
            computed_partition = algorithm(graph, n_partitions)
            _elapsed_time = time.time() - _start_time

            error_rate = Metrics.compare_partitions(
                true_labels, computed_partition)

            print(f"\tAlgorithme [{algorithm_name}]")
            print(f"\t\tError={error_rate:.2f}")
            print(f"\t\tTime={_elapsed_time:.2f}")

if __name__ == "__main__":
    main()
