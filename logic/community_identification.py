from matplotlib import pyplot as plt
import networkx as nx
from typing import List, Set, Dict, Tuple
import random

from logic.graph_generation import GraphGeneration
from logic.node_partition import NodePartition


class CommunityIdentification:
    @staticmethod
    def _init_partition(graph: nx.Graph) -> Dict[int, int]:
        """
        Initialize partition by assigning each node to its own community.
        Example:
            Input: Graph with nodes [0, 1, 2]
            Output: {0: 0, 1: 1, 2: 2}
        """
        return {node: node for node in graph.nodes()}

    @staticmethod
    def _compute_degrees(graph: nx.Graph) -> Dict[int, float]:
        """
        Compute the degree for each node using edge weights (default weight=1).
        Example:
            Input: Graph with edge (0,1)
            Output: {0: 1, 1: 1}
        """
        return {node: sum(data.get('weight', 1) for _, data in graph[node].items())
                for node in graph.nodes()}

    @staticmethod
    def _get_neighboring_communities(graph: nx.Graph, partition: Dict[int, int], node: int) -> Dict[int, float]:
        """
        Return a mapping of neighboring communities to the sum of weights
        from the given node to that community.
        Example:
            Input: Graph with edge (0,1, weight=2) and partition {0:0, 1:1}
            Output: {1: 2}
        """
        neighbor_comms = {}
        for neighbor in graph.neighbors(node):
            comm = partition[neighbor]
            weight = graph[node][neighbor].get('weight', 1)
            neighbor_comms[comm] = neighbor_comms.get(comm, 0) + weight
        return neighbor_comms

    @staticmethod
    def _one_level(graph: nx.Graph, partition: Dict[int, int], resolution: float) -> Tuple[Dict[int, int], bool]:
        """
        Perform one local moving phase of the Louvain algorithm.
        Updates the partition by moving nodes to communities that yield the highest modularity gain.
        Returns the updated partition and a flag indicating if any move was made.
        """
        m = graph.size(weight='weight')
        m = m if m > 0 else 1
        degrees = CommunityIdentification._compute_degrees(graph)
        tot = {}
        for node, comm in partition.items():
            tot[comm] = tot.get(comm, 0) + degrees[node]
        improvement = False
        nodes = list(graph.nodes())
        random.shuffle(nodes)
        for node in nodes:
            current_comm = partition[node]
            neighbor_comms = CommunityIdentification._get_neighboring_communities(
                graph, partition, node)
            tot[current_comm] -= degrees[node]
            best_comm = current_comm
            best_gain = 0.0
            for comm, dnc in neighbor_comms.items():
                gain = dnc - resolution * \
                    degrees[node] * tot.get(comm, 0) / (2 * m)
                if gain > best_gain:
                    best_gain = gain
                    best_comm = comm
            if best_comm != current_comm:
                partition[node] = best_comm
                tot[best_comm] = tot.get(best_comm, 0) + degrees[node]
                improvement = True
            else:
                tot[current_comm] += degrees[node]
        return partition, improvement

    @staticmethod
    def _aggregate_graph(graph: nx.Graph, partition: Dict[int, int]) -> nx.Graph:
        """
        Aggregate nodes by their communities to build a new graph.
        Nodes in the new graph represent communities; edge weights are summed.
        Example:
            Input: Graph with edge (0,1, weight=2) and partition {0:0, 1:0}
            Output: Graph with one node 0 and a self-loop with weight 2.
        """
        new_graph = nx.Graph()
        for comm in set(partition.values()):
            new_graph.add_node(comm)
        for u, v, data in graph.edges(data=True):
            w = data.get('weight', 1)
            cu, cv = partition[u], partition[v]
            if new_graph.has_edge(cu, cv):
                new_graph[cu][cv]['weight'] += w
            else:
                new_graph.add_edge(cu, cv, weight=w)
        return new_graph

    @staticmethod
    def louvain(graph: nx.Graph, resolution: float = 1.0) -> List[int]:
        """
        Execute the Louvain algorithm to detect communities in the graph.
        Returns a dictionary mapping each node to its community.
        Example:
            Input: A triangle graph, possible Output: {0: 0, 1: 0, 2: 0}
        """
        partition = CommunityIdentification._init_partition(graph)
        while True:
            partition, improved = CommunityIdentification._one_level(
                graph, partition, resolution)
            new_graph = CommunityIdentification._aggregate_graph(
                graph, partition)
            if new_graph.number_of_nodes() == len(graph):
                break
            new_partition = CommunityIdentification.louvain(
                new_graph, resolution)
            partition = {node: new_partition[partition[node]]
                         for node in graph.nodes()}
            break
        print(partition)
        return [partition[idx] for idx in range(len(graph.nodes))]

    @staticmethod
    def label_propagation(graph: nx.Graph) -> List[Set[int]]:
        pass  # TODO

    @staticmethod
    def girvan_newman(graph: nx.Graph, level: int = 1) -> List[Set[int]]:
        pass  # TODO

    @staticmethod
    def asynchronous_fluid(graph: nx.Graph, k: int) -> List[Set[int]]:
        pass  # TODO

###################################################################################


def display_partition(
    graph: nx.Graph,
    name: str,
    partition_list: List[List[int]] = None,
    partition_nodes: List[int] = None,
) -> None:

    if partition_list is not None:
        partition_nodes = NodePartition.partition_list_to_partition_nodes(
            partition_list)
    nx.draw(graph,
            node_color=partition_nodes,
            with_labels=True,
            cmap=plt.cm.rainbow)
    plt.title(name)


def demo():
    """
    Run a demo generating three stochastic block model graphs with varying p/q values.
    Displays the true partition (colors from the generation process) and the partition
    identified by the Louvain algorithm.
    """
    params = [
        ("Strong Communities", 40, 0.8, 0.1),
        ("Moderate Communities", 40, 0.6, 0.4),
        ("Weak Communities", 40, 0.4, 0.3)
    ]

    rows = len(params)
    plt.figure(figsize=(12, 3 * rows))
    for idx, (name, n_nodes, p, q) in enumerate(params, 1):
        true_partition = NodePartition.partition_list(
            n_nodes,
            n_partitions=4,
            as_set=False
        )

        graph = GraphGeneration.generate_stochastic_block_model(
            true_partition, p, q)

        detected_part = CommunityIdentification.louvain(graph, resolution=1.0)

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
