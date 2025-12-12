import networkx as nx
import matplotlib.pyplot as plt
import streamlit as st
import colorsys

# -------------------------------
# Generate Distinct Colors
# -------------------------------
def generate_distinct_colors(n):
    colors = []
    for i in range(n):
        hue = i / n
        r, g, b = colorsys.hsv_to_rgb(hue, 0.85, 0.95)
        colors.append('#%02x%02x%02x' % (int(r*255), int(g*255), int(b*255)))
    return colors

# -------------------------------
# Draw Graph
# -------------------------------
def draw_graph(graph, node_colors=None):
    G = nx.Graph()
    for node, neighbors in graph.items():
        for nb in neighbors:
            G.add_edge(node, nb)

    pos = nx.spring_layout(G, k=0.8, iterations=200)

    colors = [node_colors.get(node, "lightblue") for node in G.nodes] if node_colors else "lightblue"

    fig, ax = plt.subplots(figsize=(3, 2))
    nx.draw(G, pos, with_labels=True, node_color=colors, node_size=300, font_size=8, font_weight='bold', ax=ax)
    plt.tight_layout()
    st.pyplot(fig, use_container_width=False)
    plt.close(fig)

# -------------------------------
# Backtracking Coloring
# -------------------------------
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

# -------------------------------
# Streamlit App
# -------------------------------
st.set_page_config(layout="wide")
sidebar = st.sidebar
sidebar.title("Graph Coloring Details")
center_area = st.container()

# -------------------------------
# Session State Initialization
# -------------------------------
if "nodes" not in st.session_state:
    st.session_state.nodes = []
if "edges" not in st.session_state:
    st.session_state.edges = []

# -------------------------------
# Add Nodes
# -------------------------------
with center_area:
    st.header("Graph Coloring Visualizer")
    st.write("Add nodes dynamically to your graph.")

    new_node = st.text_input("Enter new node name (e.g., a, b, c)")
    if st.button("Add Node") and new_node:
        if new_node not in st.session_state.nodes:
            st.session_state.nodes.append(new_node)

# Show current nodes
sidebar.subheader("Nodes Dictionary")
dic = {node: [] for node in st.session_state.nodes}
for key in dic:
    sidebar.write(f"{key}: {dic[key]}")

# -------------------------------
# Select Edges
# -------------------------------
with center_area:
    st.subheader("Select Edges")
    with st.expander("Click to select edges"):
        for i, node in enumerate(st.session_state.nodes):
            for prev_node in st.session_state.nodes[:i]:
                key_name = f"edge_{prev_node}_{node}"
                if key_name not in st.session_state:
                    st.session_state[key_name] = False
                st.session_state[key_name] = st.checkbox(f"{prev_node} - {node}", value=st.session_state[key_name], key=key_name)
                if st.session_state[key_name]:
                    if (prev_node, node) not in st.session_state.edges and (node, prev_node) not in st.session_state.edges:
                        st.session_state.edges.append((prev_node, node))

# Update dictionary with edges
for a, b in st.session_state.edges:
    dic[a].append(b)
    dic[b].append(a)

# Show updated dictionary
sidebar.subheader("Updated Dictionary with Edges")
for key in dic:
    sidebar.write(f"{key}: {dic[key]}")

# -------------------------------
# Select Colors
# -------------------------------
with center_area:
    num_colors = st.number_input("Select number of colors", min_value=1, max_value=20, value=3)
    generated_colors = generate_distinct_colors(num_colors)
sidebar.subheader("Colors Used")
sidebar.write(generated_colors)

# -------------------------------
# Run Backtracking
# -------------------------------
if dic:
    b = Backtracking(dic, generated_colors)
    node = list(b.graph.keys())[0]
    visual_dic = b.dive(node, b.color)

    sidebar.subheader("Coloring Result")
    sidebar.write(visual_dic)

    # Draw Graph
    with center_area:
        st.subheader("Colored Graph Visualization")
        draw_graph(dic, visual_dic)
