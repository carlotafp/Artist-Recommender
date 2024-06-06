import networkx as nx
import pandas as pd
# ------- IMPLEMENT HERE ANY AUXILIARY FUNCTIONS NEEDED ------- #


# --------------- END OF AUXILIARY FUNCTIONS ------------------ #

def num_common_nodes(*arg):
    """
    Return the number of common nodes between a set of graphs.

    :param arg: (an undetermined number of) networkx graphs.
    :return: an integer, number of common nodes.
    """
    # ------- IMPLEMENT HERE THE BODY OF THE FUNCTION ------- #
    nodes = [set(graf.nodes()) for graf in arg]
    common_nodes = set.intersection(*nodes)
    return len(common_nodes)
    # ----------------- END OF FUNCTION --------------------- #


def get_degree_distribution(g: nx.Graph) -> dict:
    """
    Get the degree distribution of the graph.

    :param g: networkx graph.
    :return: dictionary with degree distribution (keys are degrees, values are number of occurrences).
    """
    # ------- IMPLEMENT HERE THE BODY OF THE FUNCTION ------- #
    dict_nodes = {}
    for node in g:
        degree = g.degree(node)
        if degree not in dict_nodes:
            dict_nodes[degree] = 1
        else:
            dict_nodes[degree] += 1

    return dict_nodes
    # ----------------- END OF FUNCTION --------------------- #


def get_k_most_central(g: nx.Graph, metric: str, num_nodes: int) -> list:
    """
    Get the k most central nodes in the graph.

    :param g: networkx graph.
    :param metric: centrality metric. Can be (at least) 'degree', 'betweenness', 'closeness' or 'eigenvector'.
    :param num_nodes: number of nodes to return.
    :return: list with the top num_nodes nodes with the specified centrality.
    """
    # ------- IMPLEMENT HERE THE BODY OF THE FUNCTION ------- #
    dicc = {}
    if metric =='degree':
        dicc = nx.degree_centrality(g)
    elif metric =='betweennes':
        dicc = nx.betweenness_centrality(g)
    elif metric == 'closeness':
        dicc = nx.closeness_centrality(g)
    elif metric == 'eigenvector':
        dicc = nx.eigenvector_centrality(g)
    dicc_ordenat = sorted(dicc.items(), key=lambda x: x[1], reverse=True)
    return dicc_ordenat[:num_nodes]
    # ----------------- END OF FUNCTION --------------------- #


def find_cliques(g: nx.Graph, min_size_clique: int) -> tuple:
    """
    Find cliques in the graph g with size at least min_size_clique.

    :param g: networkx graph.
    :param min_size_clique: minimum size of the cliques to find.
    :return: two-element tuple, list of cliques (each clique is a list of nodes) and
        list of nodes in any of the cliques.
    """
    # ------- IMPLEMENT HERE THE BODY OF THE FUNCTION ------- #
    cliques = list(nx.find_cliques(g))
    cliques_final = []
    nodes = set()
    for clique in cliques:
        if len(clique) >= min_size_clique:
            cliques_final.append(clique)
            nodes.update(clique)
    return cliques_final, list(nodes)
    # ----------------- END OF FUNCTION --------------------- #


def detect_communities(g: nx.Graph, method: str) -> tuple:
    """
    Detect communities in the graph g using the specified method.

    :param g: a networkx graph.
    :param method: string with the name of the method to use. Can be (at least) 'girvan-newman' or 'louvain'.
    :return: two-element tuple, list of communities (each community is a list of nodes) and modularity of the partition.
    """
    # ------- IMPLEMENT HERE THE BODY OF THE FUNCTION ------- #
    if method=='girvan-newman':
        particions = nx.community.girvan_newman(g)
        modularity_final= 0
        communities_final = []
        for particio in particions:
            communities = [list(community) for community in particio]
            modularity = nx.community.modularity(g, communities)
            if modularity>modularity_final:
                modularity_final = modularity
                communities_final = communities
        return communities_final, modularity_final

    elif method=='louvain':
        particio = nx.community.louvain_communities(g)
        communities = [list(community) for community in particio]
        modularity = nx.community.modularity(g,communities)
        return communities, modularity

    # ----------------- END OF FUNCTION --------------------- #


if __name__ == '__main__':
    # ------- IMPLEMENT HERE THE MAIN FOR THIS SESSION ------- #
    gB = nx.read_graphml('gB.graphml')
    gD = nx.read_graphml('gD.graphml')
    D = pd.read_csv('D.csv')
    g_b = nx.read_graphml('g\'b.graphml')
    g_d = nx.read_graphml('g\'d.graphml')
    gwB = nx.read_graphml('gwB.graphml')
    gwD = nx.read_graphml('gwD.graphml')

    print('Nodes shared between gB and gD:', num_common_nodes(gB, gD))
    print('Nodes shared between g\'b and g\'d:', num_common_nodes(g_b, g_d))
    print('Nodes shared between gwB and gwD:', num_common_nodes(gwB, gwD))
    print('Nodes shared between all the graphs:', num_common_nodes(gB, gD, g_b, g_d, gwB, gwD))
    print('Nodes shared between gB and g\'b:', num_common_nodes(gB,g_b))
    print('Nodes shared between g\'b and gwB:', num_common_nodes(g_b, gwB))

    degree = get_k_most_central(g_b,'degree',25)
    betweennes = get_k_most_central(g_b,'betweennes',25)
    a = set(node[0] for node in degree)
    b = set(node[0] for node in betweennes)
    comuns = a.intersection(b)
    print('The 25 most central nodes in the graph g\'b with degree centrality:', degree)
    print('The 25 most central nodes in the graph g\'b with betweeness centrality:', betweennes)
    print('El nombre de nodes que hi ha comuns entre els dos sets és:', len(comuns))

    cb, nb = find_cliques(g_b,7)
    cd, nd = find_cliques(g_d,7)
    print('Cliques en el graf g\'B:', len(cb))
    print ('Nombre de nodes en el clique:', len(nb))
    print('Cliques en el graf g\'D:', cd)
    print('Nombre de nodes en el clique:', (nd))

    print('Nombre component connexes a gB:',nx.number_strongly_connected_components(gB))
    print('Nombre component connexes a gD:', nx.number_strongly_connected_components(gD))
    print('nodes aïllats a gB',len([node for node in gB.nodes() if gB.out_degree(node) == 0]))
    print('nodes aïllats a gD',len([node for node in gD.nodes() if gD.out_degree(node) == 0]))
    print(nx.number_connected_components(g_d))

 # ------------------- END OF MAIN ------------------------ #
