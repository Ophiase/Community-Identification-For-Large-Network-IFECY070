from typing import Dict, List
import networkx as nx
from logic.graph_diameter import double_bfs, graph_diameter

VERBOSE = True


class TestGraphDiameter:
    @staticmethod
    def run_a_graph_test(expected: int, graph_dict: Dict[int, List[int]]):
        graph = nx.Graph(graph_dict)
        diameter = graph_diameter(graph)
        double_bfs_diameter = double_bfs(graph)

        if VERBOSE:
            print(
                f"Expected: {expected}\t Algo 1: {diameter}\t 2-BFS: {double_bfs_diameter}")

        assert diameter == expected
        assert diameter == double_bfs_diameter

    def test_0(self):
        TestGraphDiameter.run_a_graph_test(3, {
            0: [1],
            1: [0, 2],
            2: [1, 3],
            3: [2]
        })

    def test_1(self):
        TestGraphDiameter.run_a_graph_test(2, {
            0: [1, 2, 3, 4],
            1: [0],
            2: [0],
            3: [0],
            4: [0]
        })

    def test_2(self):
        TestGraphDiameter.run_a_graph_test(1, {
            0: [1, 2, 3],
            1: [0, 2, 3],
            2: [0, 1, 3],
            3: [0, 1, 2]
        })
