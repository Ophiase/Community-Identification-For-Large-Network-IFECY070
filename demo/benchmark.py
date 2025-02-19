from logic.community_identification.base import CommunityIdentification
from logic.community_identification.louvain import Louvain
from logic.graph_generation import GraphGeneration
from logic.metrics import Metrics
from logic.node_partition import NodePartition
from visualization.partition_visualization import PartitionVisualization
import time
from itertools import product
import threading


def main() -> None:
    n_values = [int(1e2), int(1e3)]  # , int(1e4)]
    param_values = [
        ("Strong Communities", 0.8, 0.1),
        ("Moderate Communities", 0.7, 0.2),
        ("Weak Communities", 0.5, 0.3)
    ]
    params = [(name, n, p, q)
              for (name, p, q), n in product(param_values, n_values)]
    timeout = 10  # in seconds

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
        print(f"{param_name}\t| {n_nodes} Nodes")

        _start_time = time.time()
        true_partition = NodePartition.partition_list(
            n_nodes, n_partitions=4, as_set=False)
        _elapsed_time_0 = time.time() - _start_time
        graph = GraphGeneration.generate_erdos_p_partition_model(
            true_partition, p, q)
        _elapsed_time_1 = time.time() - _start_time - _elapsed_time_0
        true_labels = NodePartition.partition_list_to_partition_nodes(
            true_partition, n_nodes)

        print(
            f"\tPartition ({n_partitions}) Generation Time\t= {_elapsed_time_0:.4f}")
        print(f"\tGraph Generation Time\t\t= {_elapsed_time_1:.4f}")

        for algorithm_name, algorithm in algorithms:
            computed_partition = None
            _elapsed_time = None

            def run_algorithm():
                nonlocal computed_partition
                _start_time = time.time()
                computed_partition = algorithm(graph, n_partitions)
                nonlocal _elapsed_time
                _elapsed_time = time.time() - _start_time

            thread = threading.Thread(target=run_algorithm)
            thread.start()
            thread.join(timeout=timeout)

            if thread.is_alive():
                print(f"\tAlgorithme [{algorithm_name}] timed out")
                thread.join()
                continue

            error_rate = Metrics.compare_partitions(
                true_labels, computed_partition)

            print(f"\tAlgorithme [{algorithm_name}]")
            print(f"\t\tError={error_rate:.2f}")
            print(f"\t\tTime={_elapsed_time:.2f}")


if __name__ == "__main__":
    main()
