import streamlit as st
from backtracking import Backtracking
from visualization import draw_graph  # your drawing function

# ------------------------------
# 1️⃣ Input number of nodes
# ------------------------------
n = st.number_input("Enter number of nodes", min_value=2, step=1, value=5)

# ------------------------------
# 2️⃣ Create nodes dictionary
# ------------------------------
dic = {chr(ord('a') + i): [] for i in range(n)}

# Display node dictionary horizontally
st.write("Nodes dictionary:")
num_cols_nodes = min(len(dic), 5)
cols_nodes = st.columns(num_cols_nodes)
for idx, key in enumerate(dic.keys()):
    col = cols_nodes[idx % num_cols_nodes]
    col.write(f"{key}: {dic[key]}")

# ------------------------------
# 3️⃣ Generate all possible edges
# ------------------------------
edges = []
keys = list(dic.keys())
for i in range(len(keys)):
    for j in range(i + 1, len(keys)):
        edges.append((keys[i], keys[j]))

# ------------------------------
# 4️⃣ Let user select edges (horizontal checkboxes)
# ------------------------------
st.write("Select edges to include:")
num_cols_edges = min(len(edges), 5)
cols_edges = st.columns(num_cols_edges)

selected_edges = []
for idx, edge in enumerate(edges):
    col = cols_edges[idx % num_cols_edges]
    if col.checkbox(f"{edge[0]} - {edge[1]}", value=False, key=f"edge_{idx}"):
        selected_edges.append(edge)

# ------------------------------
# 5️⃣ Update dictionary with selected edges
# ------------------------------
for a, b in selected_edges:
    dic[a].append(b)
    dic[b].append(a)

# Display updated dictionary horizontally
st.write("Updated dictionary with selected edges:")
cols_updated = st.columns(num_cols_nodes)
for idx, key in enumerate(dic.keys()):
    col = cols_updated[idx % num_cols_nodes]
    col.write(f"{key}: {dic[key]}")

# ------------------------------
# 6️⃣ Backtracking coloring
# ------------------------------
b = Backtracking(dic)
node = list(b.graph.keys())[0]
visual_dic = b.dive(node, b.color)

st.write("Graph coloring solution:")

# ------------------------------
# 7️⃣ Draw the graph
# ------------------------------
draw_graph(dic, visual_dic)
