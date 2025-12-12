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
# Draw Initial Graph (without edges)
# ----------------------------------------------------
def draw_initial_graph(nodes):
    G = nx.Graph()
    for node in nodes:
        G.add_node(node)
    
    pos = nx.spring_layout(G, k=0.8, iterations=200)
    
    fig, ax = plt.subplots(figsize=(3, 2))  # small figure
    nx.draw(
        G, pos, with_labels=True,
        node_color="lightblue", node_size=300,
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

# Create nodes dictionary (initially empty edges)
nodes = [chr(ord('a') + i) for i in range(n)]
dic = {node: [] for node in nodes}

# Sidebar shows dictionary
sidebar.subheader("Nodes Dictionary")
for key in dic:
    sidebar.write(f"{key}: {dic[key]}")


# ----------------------------------------------------
# Show initial graph with nodes only
# ----------------------------------------------------
with center_area:
    st.subheader("Initial Graph (Nodes Only)")
    draw_initial_graph(nodes)


# ----------------------------------------------------
# Colors selection (CENTER)
# ----------------------------------------------------
with center_area:
    num_colors = st.number_input("Select number of colors", min_value=1, max_value=20, value=3)
    generated_colors = generate_distinct_colors(num_colors)

# Sidebar also displays them
sidebar.subheader("Colors Used")
sidebar.write(generated_colors)


# ----------------------------------------------------
# Manually Create Edges by Selecting Nodes
# ----------------------------------------------------
with center_area:
    st.subheader("Create Edges")
    
    # Create two columns for node selection
    col1, col2, col3 = st.columns(3)
    
    with col1:
        node1 = st.selectbox("Select first node", nodes, key="node1")
    
    with col2:
        # Filter out node1 from the second node selection
        available_nodes = [n for n in nodes if n != node1]
        node2 = st.selectbox("Select second node", available_nodes, key="node2")
    
    with col3:
        if st.button("Add Edge", type="primary"):
            # Add edge if it doesn't exist
            if node2 not in dic[node1]:
                dic[node1].append(node2)
                dic[node2].append(node1)
                st.success(f"Edge added: {node1} - {node2}")
            else:
                st.warning(f"Edge {node1} - {node2} already exists!")
        
        if st.button("Remove Edge", type="secondary"):
            # Remove edge if it exists
            if node2 in dic[node1]:
                dic[node1].remove(node2)
                dic[node2].remove(node1)
                st.info(f"Edge removed: {node1} - {node2}")
            else:
                st.warning(f"Edge {node1} - {node2} doesn't exist!")

# Sidebar: updated dictionary
sidebar.subheader("Current Graph Structure")
for key in dic:
    sidebar.write(f"{key}: {dic[key]}")


# ----------------------------------------------------
# Show current edges list
# ----------------------------------------------------
with center_area:
    st.subheader("Current Edges")
    
    # Collect all edges
    current_edges = []
    for node in dic:
        for neighbor in dic[node]:
            # Add edge only once (avoid duplicates)
            edge = tuple(sorted([node, neighbor]))
            if edge not in current_edges:
                current_edges.append(edge)
    
    if current_edges:
        st.write("Edges in the graph:")
        for edge in current_edges:
            st.write(f"{edge[0]} - {edge[1]}")
    else:
        st.write("No edges added yet.")


# ----------------------------------------------------
# Run Backtracking Coloring (if graph has edges)
# ----------------------------------------------------
if current_edges:  # Only run coloring if there are edges
    b = Backtracking(dic, generated_colors)
    node = list(b.graph.keys())[0]
    visual_dic = b.dive(node, b.color)
    
    sidebar.subheader("Coloring Result")
    sidebar.write(visual_dic)
    
    # ----------------------------------------------------
    # Draw Colored Graph (CENTER) — SMALLER SIZE
    # ----------------------------------------------------
    with center_area:
        st.subheader("Colored Graph Visualization")
        draw_graph(dic, visual_dic)
else:
    with center_area:
        st.info("Add edges to the graph to see the coloring result.")
        # Draw empty graph
        st.subheader("Current Graph")
        draw_initial_graph(nodes)
