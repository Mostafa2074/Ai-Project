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
# Draw Graph Function (SMALLER VISUAL)
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

    # Smaller figure
    fig, ax = plt.subplots(figsize=(3, 2))  # small figure
    nx.draw(
        G, pos, with_labels=True,
        node_color=colors, node_size=300,
        font_size=8, font_weight='bold',
        ax=ax
    )
    plt.tight_layout()

    # VERY IMPORTANT: use_container_width=False keeps it small
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
# PAGE LAYOUT
# ----------------------------------------------------
st.set_page_config(layout="wide")

sidebar = st.sidebar
sidebar.title("Graph Coloring Details")
center_area = st.container()


# ----------------------------------------------------
# UI Input - Number of Nodes (CENTER)
# ----------------------------------------------------
with center_area:
    st.header("Graph Coloring Visualizer")
    st.write("Customize the graph and choose coloring options.")

    n = st.number_input("Enter number of nodes", min_value=2, step=1, value=5)

# Create nodes dictionary
dic = {chr(ord('a') + i): [] for i in range(n)}

# Sidebar shows dictionary
sidebar.subheader("Nodes Dictionary")
for key in dic:
    sidebar.write(f"{key}: {dic[key]}")


# ----------------------------------------------------
# Colors selection (CENTER) — NO PRINTING IN CENTER
# ----------------------------------------------------
with center_area:
    num_colors = st.number_input("Select number of colors", min_value=1, max_value=20, value=3)
    generated_colors = generate_distinct_colors(num_colors)

# Sidebar also displays them
sidebar.subheader("Colors Used")
sidebar.write(generated_colors)


# ----------------------------------------------------
# Generate All Possible Edges
# ----------------------------------------------------
edges = []
keys = list(dic.keys())
for i in range(len(keys)):
    for j in range(i + 1, len(keys)):
        edges.append((keys[i], keys[j]))

# CENTER: select edges
# CENTER: select edges inside an expander
with center_area:
    st.subheader("Select Edges")
    
    # Collapsible section
    with st.expander("Click to select edges"):
        selected_edges = []
        for idx, edge in enumerate(edges):
            if st.checkbox(f"{edge[0]} - {edge[1]}", value=False, key=f"edge_{idx}"):
                selected_edges.append(edge)


# Update dictionary
for a, b in selected_edges:
    dic[a].append(b)
    dic[b].append(a)

# Sidebar: updated dictionary
sidebar.subheader("Updated Dictionary with Edges")
for key in dic:
    sidebar.write(f"{key}: {dic[key]}")


# ----------------------------------------------------
# Run Backtracking Coloring
# ----------------------------------------------------
b = Backtracking(dic, generated_colors)
node = list(b.graph.keys())[0]
visual_dic = b.dive(node, b.color)

sidebar.subheader("Coloring Result")
sidebar.write(visual_dic)


# ----------------------------------------------------
# Draw Graph (CENTER) — SMALLER SIZE
# ----------------------------------------------------
with center_area:
    st.subheader("Colored Graph Visualization")
    draw_graph(dic, visual_dic)
