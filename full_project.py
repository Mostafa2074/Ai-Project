import networkx as nx
import matplotlib.pyplot as plt
import streamlit as st
import colorsys

# ----------------------------------------------------
# Generate Distinct Colors
# ----------------------------------------------------
def generate_distinct_colors(n):
    colors = []
    for i in range(n):
        hue = i / n
        r, g, b = colorsys.hsv_to_rgb(hue, 0.85, 0.95)
        colors.append('#%02x%02x%02x' % (int(r*255), int(g*255), int(b*255)))
    return colors

# ----------------------------------------------------
# Draw Graph Function (Small Visual)
# ----------------------------------------------------
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

    fig, ax = plt.subplots(figsize=(3, 2))
    nx.draw(
        G, pos, with_labels=True,
        node_color=colors, node_size=300,
        font_size=8, font_weight='bold',
        ax=ax
    )
    plt.tight_layout()
    st.pyplot(fig, use_container_width=False)
    plt.close(fig)

# ----------------------------------------------------
# Backtracking Class
# ----------------------------------------------------
class Backtracking:
    def __init__(self, graph, colors):
        self.graph = graph
        self.explored = {}
        self.color = colors

    def dive(self, node, colors):
        clr = self.search(node, colors)
        if clr is None:
            return None
        else:
            self.explored[node] = clr[0]

        if len(self.explored) == len(self.graph):
            return self.explored

        for i in self.graph[node]:
            if i not in self.explored:
                temp = self.dive(i, self.color)
                if temp is None:
                    keys = list(self.explored.keys())
                    k = keys.index(node)
                    slice_keys = keys[k:]
                    for key in slice_keys:
                        del self.explored[key]
                    return self.dive(node, clr[1:])
        return self.explored

    def search(self, node, colors):
        temp_color = colors.copy()
        for i in self.graph[node]:
            if i in self.explored:
                try:
                    temp_color.remove(self.explored[i])
                except:
                    pass
        return temp_color if temp_color else None

# ----------------------------------------------------
# Page layout
# ----------------------------------------------------
st.set_page_config(layout="wide")

sidebar = st.sidebar
sidebar.title("Graph Inputs & Details")
center_area = st.container()

# ----------------------------------------------------
# Sidebar: Inputs
# ----------------------------------------------------
num_nodes = sidebar.number_input("Number of Nodes", min_value=2, step=1, value=5)
num_colors = sidebar.number_input("Number of Colors", min_value=1, max_value=20, value=3)

# Generate nodes and colors
dic = {chr(ord('a') + i): [] for i in range(num_nodes)}
generated_colors = generate_distinct_colors(num_colors)

# Show node and color details in sidebar
# sidebar.subheader("Nodes Dictionary")
# for key in dic:
#     sidebar.write(f"{key}: {dic[key]}")

# sidebar.subheader("Colors Used")
# sidebar.write(generated_colors)

# ----------------------------------------------------
# Generate All Possible Edges
# ----------------------------------------------------
edges = []
keys = list(dic.keys())
for i in range(len(keys)):
    for j in range(i + 1, len(keys)):
        edges.append((keys[i], keys[j]))

# ----------------------------------------------------
# Main Area: Edge Selection in Expander
# ----------------------------------------------------
with center_area:
    st.header("Graph Coloring Visualizer")
    st.subheader("Select edges for your graph")

    selected_edges = []
    with st.expander("Click to select edges"):
        for idx, edge in enumerate(edges):
            if st.checkbox(f"{edge[0]} - {edge[1]}", value=False, key=f"edge_{idx}"):
                selected_edges.append(edge)

# Update adjacency list
for a, b in selected_edges:
    dic[a].append(b)
    dic[b].append(a)

# Sidebar: show updated dictionary
# sidebar.subheader("Updated Dictionary with Edges")
# for key in dic:
#     sidebar.write(f"{key}: {dic[key]}")

# ----------------------------------------------------
# Backtracking coloring
# ----------------------------------------------------
b = Backtracking(dic, generated_colors)
start_node = list(dic.keys())[0]
visual_dic = b.dive(start_node, b.color)

sidebar.subheader("Graph Coloring Result")
sidebar.write(visual_dic)

# ----------------------------------------------------
# Draw Graph in Main Area
# ----------------------------------------------------
with center_area:
    st.subheader("Colored Graph Visualization")
    draw_graph(dic, visual_dic)


