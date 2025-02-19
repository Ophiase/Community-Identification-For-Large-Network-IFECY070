import os
import time
import pandas as pd
from multiprocessing import Process, Queue
from typing import Any, Callable, Optional, Tuple, List
from itertools import product

from logic.community_identification.base import CommunityIdentification
from logic.community_identification.girvan_newman import GirvanNewman
from logic.community_identification.label_propagation import LabelPropagation
from logic.community_identification.louvain import Louvain
from logic.graph_generation import GraphGeneration
from logic.metrics import Metrics
from logic.node_partition import NodePartition
from visualization.partition_visualization import PartitionVisualization

BENCHMARK_OUTPUT: str = os.path.join("output", "benchmark.csv")
TIMEOUT: float = 1.0


def execute_with_timeout(
        func: Callable[..., Any],
        timeout: float,
        *args: Any,
        **kwargs: Any
) -> Tuple[Optional[Any], Optional[float]]:
    queue: Queue = Queue()

    def worker(q: Queue, *args: Any, **kwargs: Any) -> None:
        start: float = time.time()
        result: Any = func(*args, **kwargs)
        q.put((result, time.time() - start))

    process: Process = Process(
        target=worker, args=(queue,)+args, kwargs=kwargs)
    process.start()
    process.join(timeout)
    if process.is_alive():
        process.terminate()
        process.join()
        return None, None
    return queue.get() if not queue.empty() else (None, None)


def process_parameters(
        params: List[Tuple[str, int, float, float]],
        algorithms: List[Tuple[str, Callable[[Any, int], Any]]]
) -> List[dict]:

    benchmark_data: List[dict] = []

    for param_name, n_nodes, p, q in params:
        print(f"{param_name}\t| {n_nodes} Nodes")
        start_time: float = time.time()
        true_partition: List[Any] = NodePartition.partition_list(
            n_nodes, n_partitions=4, as_set=False)
        elapsed_partition: float = time.time() - start_time
        graph: Any = GraphGeneration.generate_erdos_p_partition_model(
            true_partition, p, q)
        elapsed_graph: float = time.time() - start_time - elapsed_partition
        true_labels: Any = NodePartition.partition_list_to_partition_nodes(
            true_partition, n_nodes)
        print(f"\tPartition Generation Time\t= {elapsed_partition:.4f}")
        print(f"\tGraph Generation Time\t\t= {elapsed_graph:.4f}")
        for algorithm_name, algorithm in algorithms:
            # type: ignore
            result, elapsed = execute_with_timeout(
                algorithm, TIMEOUT, graph, 4)  # type: ignore
            if result is None:
                print(f"\tAlgorithm [{algorithm_name}] timed out")
            else:
                error_rate: float = Metrics.compare_partitions(
                    true_labels, result)
                print(f"\tAlgorithm [{algorithm_name}]")
                print(f"\t\tError={error_rate:.2f}")
                print(f"\t\tTime={elapsed:.2f}")
            benchmark_data.append({
                "community_label": param_name,
                "n_nodes": n_nodes,
                "p": p,
                "q": q,
                "algorithm": algorithm_name,
                "error": error_rate if result is not None else None,
                "time": elapsed if result is not None else None
            })
    return benchmark_data


def save_benchmark(
        benchmark_data: List[dict],
        output_path: str = BENCHMARK_OUTPUT
) -> None:
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    pd.DataFrame(benchmark_data).to_csv(output_path, index=False)
    print(f"Saving to {output_path} ..")


def main() -> None:
    n_values: List[int] = [int(1e2), int(1e3)]
    param_values: List[Tuple[str, float, float]] = [
        ("Strong Communities", 0.8, 0.1),
        ("Moderate Communities", 0.7, 0.2),
        ("Weak Communities", 0.5, 0.3)
    ]

    params: List[Tuple[str, int, float, float]] = [
        (name, n, p, q) for (name, p, q), n in product(param_values, n_values)]
    algorithms: List[Tuple[str, Callable[[Any, int], Any]]] = [
        ("Louvain", lambda graph, n_parts: CommunityIdentification.project_partition(
            n_parts, Louvain.identification(graph, resolution=1.0))),
        ("Label Propagation", lambda graph, n_parts: CommunityIdentification.project_partition(
            n_parts, LabelPropagation.identification(graph))),
        ("Girvan Newman", lambda graph, n_parts: CommunityIdentification.project_partition(
            n_parts, NodePartition.partition_list_to_partition_nodes(GirvanNewman.identification(graph))))
    ]

    benchmark_data: List[dict] = process_parameters(params, algorithms)
    save_benchmark(benchmark_data)


if __name__ == "__main__":
    main()
