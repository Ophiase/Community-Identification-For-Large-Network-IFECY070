from logic.bfs import bfs
import networkx as nx


class TestBFS:
    def test_001(self):
        tree = nx.Graph({
            0: [1, 2],
            1: [0, 3, 4],
            2: [0, 5],
            3: [1],
            4: [1],
            5: [2],
            6: [2]
        })

        result = bfs(tree, 0)

        assert (result == {
            0: 0,
            1: 1,
            2: 1,
            3: 2,
            4: 2,
            5: 2,
            6: 2})
