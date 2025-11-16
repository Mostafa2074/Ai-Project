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

class Backtracking:

    def __init__(self, graph):
        self.graph = graph
        self.explored = {}
        self.color = ['red', 'blue', 'green']

    def dive(self, node, colors):
        print(node)
        print(self.explored)
        
        clr = self.search(node, colors)
        if clr == None:
            return None
        else:
            self.explored[node] = clr[0]    
        if len(list(self.explored.keys())) == len(list(self.graph.keys())):
            return self.explored
    
        else:
            for i in self.graph[node]:
                if i not in list(self.explored.keys()):
                    print(i,'kk')
                    temp = self.dive(i, self.color)
                    if temp == None:
                        keys = list(self.explored.keys())
                        k = keys.index(node)
                        slice_keys = keys[k:]
                        for key in slice_keys:
                            del self.explored[key] 
                        # del explored[node]
                        return self.dive(node, clr[1:])
                
            return self.explored
                

    def search(self, node, colors):
        temp_color = colors.copy()
        for i in self.graph[node]:
            if i in list(self.explored.keys()):
                try:
                    temp_color.remove(self.explored[i])
                except:
                    pass    

        if len(temp_color)==0:
            return None
        else:
            return temp_color       


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