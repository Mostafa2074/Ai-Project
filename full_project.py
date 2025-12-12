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
# Sidebar Inputs
# ----------------------------------------------------
num_nodes = sidebar.number_input("Number of Nodes", min_value=2, step=1, value=5)
num_colors = sidebar.number_input("Number of Colors", min_value=1, max_value=20, value=3)
generated_colors = generate_distinct_colors(num_colors)

# ----------------------------------------------------
# Initialize session state
# ----------------------------------------------------
if 'dic' not in st.session_state:
    st.session_state.dic = {}
if 'edge_state' not in st.session_state:
    st.session_state.edge_state = {}

# Add new nodes if num_nodes increased
for i in range(len(st.session_state.dic), num_nodes):
    new_node = chr(ord('a') + i)
    st.session_state.dic[new_node] = {}

# Generate all possible edges for current nodes
keys = list(st.session_state.dic.keys())
edges = []
for i in range(len(keys)):
    for j in range(i + 1, len(keys)):
        edges.append((keys[i], keys[j]))
        # initialize checkbox state
        if (keys[i], keys[j]) not in st.session_state.edge_state:
            st.session_state.edge_state[(keys[i], keys[j])] = False

# ----------------------------------------------------
# Main Area: Edge selection in Expander
# ----------------------------------------------------
selected_edges = []

with center_area:
    st.header("Graph Coloring Visualizer")
    st.subheader("Select edges for your graph")

    with st.expander("Click to select edges"):
        for a, b in edges:
            key = (a, b)
            st.session_state.edge_state[key] = st.checkbox(f"{a} - {b}", value=st.session_state.edge_state[key], key=f"{a}_{b}")
            if st.session_state.edge_state[key]:
                selected_edges.append((a, b))

# ----------------------------------------------------
# Update adjacency dictionary
# ----------------------------------------------------
dic = {k: [] for k in st.session_state.dic.keys()}
for a, b in selected_edges:
    dic[a].append(b)
    dic[b].append(a)

# ----------------------------------------------------
# Backtracking coloring
# ----------------------------------------------------
b = Backtracking(dic, generated_colors)
start_node = list(dic.keys())[0]
visual_dic = b.dive(start_node, b.color)

# ----------------------------------------------------
# Draw Graph in Main Area
# ----------------------------------------------------
with center_area:
    st.subheader("Colored Graph Visualization")
    draw_graph(dic, visual_dic)
