from typing import List, Tuple, Union

import matplotlib.pyplot as plt
import networkx as nx

from FunctionCall import FunctionCall
from Process import Process


class Grapher:
    def __init__(self):
        self.edges: List[Tuple[Union[Process, FunctionCall], FunctionCall]] = []

    def add_processes(self, processes: List[Process]):
        for proc in processes:
            self._recurse_add_children(proc)

    def _recurse_add_children(self, parent: Union[Process, FunctionCall]):
        for child in parent.children:
            self.edges.append((parent, child))
            self._recurse_add_children(child)

    def draw(self):
        graph = nx.DiGraph()
        graph.add_edges_from(self.edges)
        positions = nx.planar_layout(graph)
        nx.draw_networkx(graph, positions)
        plt.show()

    def test_draw(self):
        graph = nx.DiGraph()
        my_edges = self.edges[:100]
        graph.add_edges_from(my_edges)

        positions = nx.planar_layout(graph)
        nx.draw_networkx(graph, positions)
        plt.show()
