import networkx as nx
import matplotlib.pyplot as plt
import streamlit as st
import random
import colorsys


# ----------------------------------------------------
# Generate Distinct Colors (Not Similar)
# ----------------------------------------------------
def generate_distinct_colors(n):
    colors = []
    for i in range(n):
        hue = i / n                      # evenly spaced hues
        r, g, b = colorsys.hsv_to_rgb(hue, 0.85, 0.95)
        colors.append('#%02x%02x%02x' % (int(r*255), int(g*255), int(b*255)))
    return colors


# ----------------------------------------------------
# Draw Graph Function
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

    plt.figure(figsize=(8, 6))
    nx.draw(
        G, pos, with_labels=True,
        node_color=colors, node_size=800,
        font_size=12, font_weight='bold'
    )

    st.pyplot(plt)
    plt.close()


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

        if len(temp_color) == 0:
            return None
        else:
            return temp_color


# ----------------------------------------------------
# UI Input - Number of Nodes
# ----------------------------------------------------
n = st.number_input("Enter number of nodes", min_value=2, step=1, value=5)

# Create nodes dictionary
dic = {chr(ord('a') + i): [] for i in range(n)}

# Display nodes dictionary
st.write("Nodes dictionary:")
num_cols_nodes = min(len(dic), 5)
cols_nodes = st.columns(num_cols_nodes)
for idx, key in enumerate(dic.keys()):
    col = cols_nodes[idx % num_cols_nodes]
    col.write(f"{key}: {dic[key]}")

# ----------------------------------------------------
# UI Input - Number of Colors (Distinct Colors)
# ----------------------------------------------------
num_colors = st.number_input("Select number of colors", min_value=1, max_value=20, value=3)
generated_colors = generate_distinct_colors(num_colors)
st.write("Generated Distinct Colors:", generated_colors)

# ----------------------------------------------------
# Generate All Possible Edges
# ----------------------------------------------------
edges = []
keys = list(dic.keys())
for i in range(len(keys)):
    for j in range(i + 1, len(keys)):
        edges.append((keys[i], keys[j]))

# Select edges
st.write("Select edges to include:")
num_cols_edges = min(len(edges), 5)
cols_edges = st.columns(num_cols_edges)

selected_edges = []
for idx, edge in enumerate(edges):
    col = cols_edges[idx % num_cols_edges]
    if col.checkbox(f"{edge[0]} - {edge[1]}", value=False, key=f"edge_{idx}"):
        selected_edges.append(edge)

# Update dictionary with selected edges
for a, b in selected_edges:
    dic[a].append(b)
    dic[b].append(a)

# Display updated dictionary
st.write("Updated dictionary with selected edges:")
cols_updated = st.columns(num_cols_nodes)
for idx, key in enumerate(dic.keys()):
    col = cols_updated[idx % num_cols_nodes]
    col.write(f"{key}: {dic[key]}")

# ----------------------------------------------------
# Run Backtracking Coloring
# ----------------------------------------------------
b = Backtracking(dic, generated_colors)
node = list(b.graph.keys())[0]
visual_dic = b.dive(node, b.color)

st.write("Graph coloring solution:")
st.write(visual_dic)

# ----------------------------------------------------
# Draw Graph
# ----------------------------------------------------
draw_graph(dic, visual_dic)
