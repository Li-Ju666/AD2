import networkx as nx

def create_graph():
    G = nx.Graph()
    G.add_edge('a', 'b', weight=0.6)
    G.add_edge('a', 'c', weight=0.2)
    G.add_edge('c', 'd', weight=0.1)
    G.add_edge('c', 'e', weight=0.7)
    G.add_edge('c', 'f', weight=0.9)
    G.add_edge('a', 'd', weight=0.3)
    return G

def update_MST_4(G, T, e, w):
    (u, v) = e
    assert (e in G.edges() and e in T.edges())

    G.add_edge(*e, weight = w)
    T.remove_edge(u, v)
    print(list(T.edges))
    print(list(T.adj['a']))


    def explore(node, parent):
        block = [node]
        son = list(T.adj[node])
        if parent is not None:
            son.remove(parent)

        for each in son:
            block = block + explore(each, node)
        return block

    block1 = explore(u, None)
    block2 = explore(v, None)
    print('block1 contains nodes: ', block1)
    print('block2 contains nodes: ', block2)

    dic = dict.fromkeys(block1, -1)
    dic.update(dict.fromkeys(block2, 1))
    print('dictionary is: ', dic)
    edges = list(G.edges)
    cut_set = []
    for each in edges:
        if dic[each[0]]+dic[each[1]] == 0:
            cut_set.append(each)
    print(type(cut_set[0]))
    weight = []
    for each in cut_set:
        weight.append(G.edges[each]['weight'])
    print(weight)
    T.add_edge(*cut_set[weight.index(min(weight))], weight = min(weight))
    return None



G = create_graph()
T = nx.minimum_spanning_tree(G)
T = update_MST_4(G, T, ('a', 'c'), 0.4)
print(T.edges)
