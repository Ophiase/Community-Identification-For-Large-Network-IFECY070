import matplotlib.pyplot as plt
from collections import defaultdict
import random
from typing import Dict
import networkx as nx
import sys

from .bfs import bfs_restricted
from .graph_generation import GraphGeneration

###################################################################################


class DegreeDistribution:
    def distribution(graph: nx.Graph, num_destinations: int) -> Dict[int, int]:
        """
        Compute the degree distribution from a restricted BFS on a given graph.

        Args:
            graph: The NetworkX graph object.
            num_destinations: The number of destination nodes to consider.

        Returns:
            A dictionary where the keys are degrees, and the values are the number of nodes with that degree.
        """
        # Select random start node and destinations
        nodes = list(graph.nodes)
        start_node = random.choice(nodes)
        destinations = set(random.sample(
            nodes, min(num_destinations, len(nodes))))

        # Perform restricted BFS
        restricted_result = bfs_restricted(graph, start_node, destinations)

        # Calculate degree distribution
        degree_count = defaultdict(int)
        for node in restricted_result:
            degree = graph.degree[node]
            degree_count[degree] += 1

        return dict(degree_count)

    def plot(distribution: Dict[int, int]) -> None:
        degrees = list(distribution.keys())
        counts = list(distribution.values())

        plt.figure(figsize=(10, 6))
        plt.bar(degrees, counts, color='blue', edgecolor='black')
        plt.xlabel('Degree')
        plt.ylabel('Number of Nodes')
        plt.title('Degree Distribution')
        plt.grid(True)
        plt.show()

###################################################################################


def compute(graph: nx.Graph, num_destinations: int):
    distribution = DegreeDistribution.distribution(graph, num_destinations)

    print("Degree Distribution:")
    for degree, count in sorted(distribution.items()):
        print(f"Degree {degree}: {count} nodes")

    DegreeDistribution.plot(distribution)


def test():
    graph = GraphGeneration.erdos_graph_m(100, 500)
    # graph = GraphGeneration.tp3_graph(100, 0.9, 0.1)
    compute(graph, 10)


def main() -> None:
    if len(sys.argv) != 3:
        print("Usage: python script.py <graph_file> <num_destinations>")
        sys.exit(1)

    graph = nx.read_edgelist(sys.argv[1], nodetype=1)
    num_destinations = int(sys.argv[2])

    compute(graph, num_destinations)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        test()
    else:
        main()
