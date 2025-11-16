# g = {'a': ['b', 'c', 'd'], 'b': ['a', 'e', 'f'], 'c': ['a', 'f'], 'd': ['a', 'h'], 'e': ['b'], 'f': ['b', 'c'], 'h':['d', 'i'], 'i': ['h']}
# g = {'a': ['b', 'c', 'd'], 'b': ['a', 'e', 'f'], 'c': ['a'], 'd': ['a', 'h'], 'e': ['b'], 'f': ['b'], 'h':['d', 'i'], 'i': ['h']}
# g = {'a': ['b', 'c', 'd'], 'b': ['a', 'e', 'c'], 'c': ['a', 'b', 'g', 'h', 'd'], 'd': ['a', 'c', 'f', 'j'], 'e': ['b', 'f', 'h'], 'f': ['e', 'g', 'd'], 'g':['c', 'i', 'f'], 'h': ['e', 'c', 'j'], 'i':['b', 'g', 'j'], 'j': ['i', 'h', 'd']}
# g = {'a': ['b', 'c'], 'b': ['a', 'e', 'c', 'i'], 'c': ['a', 'b', 'g', 'h', 'd'], 'd': ['c', 'f'], 'e': ['b', 'f', 'h'], 'f': ['e', 'g', 'd'], 'g':['c', 'i', 'f'], 'h': ['e', 'c', 'j'], 'i':['b', 'g', 'j'], 'j': ['i', 'h']}
# g = {'a': ['d', 'b'], 'b': ['a', 'c', 'e'], 'c': ['d', 'b', 'e'], 'd': ['a', 'c'], 'e': ['b', 'c']}
# g = {'a':['b', 'c', 'd'], 'b':['a', 'c', 'e'], 'c':['a', 'b'], 'd':['a', 'f', 'e'], 'e':['b', 'd'], 'f':['d']}
# g = {'a':['b', 'e', 'd'], 'b':['a', 'c'], 'c':['b', 'd', 'f'], 'd':['a', 'c', 'e', 'f'], 'e':['a', 'd', 'f'], 'f':['c', 'd', 'e']}

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


b = Backtracking({'a':['b', 'e', 'd'], 'b':['a', 'c'], 'c':['b', 'd', 'f'], 'd':['a', 'c', 'e', 'f'], 'e':['a', 'd', 'f'], 'f':['c', 'd', 'e']})
print(b.dive('a', b.color))
# print(b.explored)             