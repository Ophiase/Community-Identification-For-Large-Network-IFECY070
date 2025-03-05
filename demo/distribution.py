
import sys
from logic.degree_distribution import DegreeDistribution
from logic.graph_generation import GraphGeneration
import networkx as nx


def compute(graph: nx.Graph, num_destinations: int):
    distribution = DegreeDistribution.distribution(graph, num_destinations)

    print("Degree Distribution:")
    for degree, count in sorted(distribution.items()):
        print(f"- Degree {degree}: {count} nodes")

    DegreeDistribution.plot(distribution)


def test():
    N=100
    M=500
    print(f"Generate an erdos graph G(n={N}, m={M}) ")
    graph = GraphGeneration.erdos_graph_m(N, M)
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
