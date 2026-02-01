import networkx as nx
import matplotlib.pyplot as plt
import os

def create_graph(dependencies):
    os.makedirs("docs", exist_ok=True)

    G = nx.DiGraph()

    for file, calls in dependencies.items():
        for call in calls:
            G.add_edge(file.split("/")[-1], call)

    plt.figure(figsize=(14, 10))
    nx.draw(G, with_labels=True, node_size=2500, font_size=8)
    plt.savefig("docs/dependency_graph.png")
