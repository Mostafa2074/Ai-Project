import networkx as nx
import matplotlib.pyplot as plt
import streamlit as st


def draw_graph(graph, node_colors=None):
    G = nx.Graph()
    for node, neighbors in graph.items():
        for nb in neighbors:
            G.add_edge(node, nb)

    pos = nx.spring_layout(G, k=0.8, iterations=200)

    if node_colors:
        colors = [node_colors.get(node, "lightblue") for node in G.nodes]
    else:
        colors = "lightblue"

    plt.figure(figsize=(8, 6))
    nx.draw(
        G, pos, with_labels=True,
        node_color=colors, node_size=800,
        font_size=12, font_weight='bold'
    )
    
    st.pyplot(plt)  # <-- Streamlit displays the figure
    plt.close()