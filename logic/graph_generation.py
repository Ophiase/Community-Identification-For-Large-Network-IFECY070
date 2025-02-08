import networkx as nx
import random
import matplotlib.pyplot as plt


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


def main():
    n_vertices = 10
    probability = 0.3
    g = erdos_graph_p(n_vertices, probability)

    plt.subplot(121)
    nx.draw(g, with_labels=True)
    plt.title("Erdos-Renyi Graph with p")

    #########################################

    m_edges = 15
    g_m = erdos_graph_m(n_vertices, m_edges)

    plt.subplot(122)
    nx.draw(g_m, with_labels=True)
    plt.title("Erdos-Renyi Graph with m")

    plt.show()


if __name__ == "__main__":
    main()
