import networkx as nx
import matplotlib.pyplot as plt
import streamlit as st
import random
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
# Draw Graph Function
# ----------------------------------------------------
# ----------------------------------------------------
# Draw Graph Function (SMALLER VISUAL)
# ----------------------------------------------------
# ----------------------------------------------------
# Draw Graph Function (SMALLER AND CENTERED)
# ----------------------------------------------------
def draw_graph(graph, node_colors=None):
    # Create the NetworkX graph
    G = nx.Graph()
    for node, neighbors in graph.items():
        for nb in neighbors:
            G.add_edge(node, nb)

    # Layout positions
    pos = nx.spring_layout(G, k=0.8, iterations=200)

    # Node colors
    if node_colors:
        colors = [node_colors.get(node, "lightblue") for node in G.nodes]
    else:
        colors = "lightblue"

    # Create 3 columns to center the figure
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:  # Center column
        # Smaller figure
        fig, ax = plt.subplots(figsize=(3, 2))  # compact figure
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
# Streamlit Layout
# ----------------------------------------------------
st.set_page_config(layout="wide")
sidebar = st.sidebar
center_area = st.container()

# Sidebar Inputs
sidebar.title("Graph Coloring Options")

# Number of nodes
num_nodes = sidebar.number_input("Number of nodes", min_value=2, step=1, value=5)

# Create nodes dictionary
dic = {chr(ord('a') + i): [] for i in range(num_nodes)}

# Number of colors
num_colors = sidebar.number_input("Number of colors", min_value=1, max_value=20, value=3)
generated_colors = generate_distinct_colors(num_colors)

# Edge selection in sidebar
sidebar.subheader("Select Edges")
edges = []
keys = list(dic.keys())
for i in range(len(keys)):
    for j in range(i + 1, len(keys)):
        edges.append((keys[i], keys[j]))

selected_edges = []
for idx, edge in enumerate(edges):
    if sidebar.checkbox(f"{edge[0]} - {edge[1]}", value=False, key=f"edge_{idx}"):
        selected_edges.append(edge)

# Update dictionary with selected edges
for a, b in selected_edges:
    dic[a].append(b)
    dic[b].append(a)

# Sidebar display of dictionary and colors
sidebar.subheader("Nodes Dictionary with Edges")
for key in dic:
    sidebar.write(f"{key}: {dic[key]}")

sidebar.subheader("Colors Used")
sidebar.write(generated_colors)

# Run Backtracking
b = Backtracking(dic, generated_colors)
node = list(b.graph.keys())[0]
visual_dic = b.dive(node, b.color)

sidebar.subheader("Coloring Result")
sidebar.write(visual_dic)

# Center area: visualization only
with center_area:
    st.header("Graph Visualization")
    draw_graph(dic, visual_dic)


