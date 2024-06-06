import networkx as nx
import pandas as pd
import numpy as np
from scipy.spatial.distance import euclidean
# ------- IMPLEMENT HERE ANY AUXILIARY FUNCTIONS NEEDED ------- #

# --------------- END OF AUXILIARY FUNCTIONS ------------------ #

def retrieve_bidirectional_edges(g: nx.DiGraph, out_filename: str) -> nx.Graph:
    """
    Convert a directed graph into an undirected graph by considering bidirectional edges only.

    :param g: a networkx digraph.
    :param out_filename: name of the file that will be saved.
    :return: a networkx undirected graph.
    """
    # ------- IMPLEMENT HERE THE BODY OF THE FUNCTION ------- #
    #CREEM PRIMER LA LLISTA D'ARESTES QUE AFEGIREM
    bi_edges = []
    for ni, nf in g.edges():
        if g.has_edge(nf,ni):
            bi_edges.append((ni,nf))

    #CREEM GRAF NO DIRECCIONAL
    unigraf = nx.Graph()
    for n1, n2 in bi_edges:
        if n1 not in unigraf.nodes():
            unigraf.add_node(n1)
        if n2 not in unigraf.nodes():
            unigraf.add_node(n2)
        unigraf.add_edge(n1,n2)

    nx.write_graphml(unigraf, out_filename)
    return unigraf
    # ----------------- END OF FUNCTION --------------------- #


def prune_low_degree_nodes(g: nx.Graph, min_degree: int, out_filename: str) -> nx.Graph:
    """
    Prune a graph by removing nodes with degree < min_degree.

    :param g: a networkx graph.
    :param min_degree: lower bound value for the degree.
    :param out_filename: name of the file that will be saved.
    :return: a pruned networkx graph.
    """
    # ------- IMPLEMENT HERE THE BODY OF THE FUNCTION ------- #
    #Iterem per cada node, i si el seu grau és més petit que min_degree, l'afegim a la llista nodes_borrar
    nodes_borrar_lowdegree = [node for node in g.nodes() if g.degree(node) < min_degree]

    #Borrem tots els nodes de la llista nodes_borrar_lowdegree, que són els nodes que no compleixen el mínim
    g.remove_nodes_from(nodes_borrar_lowdegree)

    #Iterem un altre cop per tots els nodes i borrem aquells que tenen grau 0
    nodes_borrar_zerodegree = [node for node in g.nodes() if g.degree(node) == 0]
    g.remove_nodes_from(nodes_borrar_zerodegree)
    nx.write_graphml(g, out_filename)
    return g
    # ----------------- END OF FUNCTION --------------------- #

def prune_low_weight_edges(g: nx.Graph, min_weight=None, min_percentile=None, out_filename: str = None) -> nx.Graph:
    """
    Prune a graph by removing edges with weight < threshold. Threshold can be specified as a value or as a percentile.

    :param g: a weighted networkx graph.
    :param min_weight: lower bound value for the weight.
    :param min_percentile: lower bound percentile for the weight.
    :param out_filename: name of the file that will be saved.
    :return: a pruned networkx graph.
    """
    # ------- IMPLEMENT HERE THE BODY OF THE FUNCTION -------
    # Si els paràmetres min_weight i min_percentile estan buits o plens a la vegada, fem un raise Exception
    if (min_weight == None and min_percentile == None) or (min_weight != None and min_percentile != None):
        raise Exception('The function call should only specify one of the two parameters')
    #Si el min_percentile no és None, transformem el min_percentile a un min_weight
    if min_percentile != None:
        weights = [d['weight'] for (u, v, d) in g.edges(data=True)]
        min_weight = np.percentile(weights, min_percentile)
    #Borrem les arestes que tinguin un weight més petit al min_weight, després borrem els nodes de grau zero
    edges_borrar_loweight = [(u,v) for (u,v,d) in g.edges(data=True) if d["weight"] < min_weight]
    g.remove_edges_from(edges_borrar_loweight)
    nodes_borrar_zerodegree = [node for node in g.nodes() if g.degree(node) == 0]
    g.remove_nodes_from(nodes_borrar_zerodegree)
    nx.write_graphml(g, out_filename)
    return g
    # ----------------- END OF FUNCTION --------------------- #
def compute_mean_audio_features(tracks_df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute the mean audio features for tracks of the same artist.

    :param tracks_df: tracks dataframe (with audio features per each track).
    :return: artist dataframe (with mean audio features per each artist).
    """
    # ------- IMPLEMENT HERE THE BODY OF THE FUNCTION ------- #
    #Creem un nou datagrama agrupant per diferents grups els artistes i Id, després calculem la mitjana de cada audio feature, i s'afegeix tmb
    columnes=['song_duration', 'song_popularity', 'album_id','album_name','album_release_date', 'song_id', 'song_name']
    audio_features_df = tracks_df.drop(columns=columnes)
    df = audio_features_df.groupby(['artist_id','artist_name']).mean()
    return df
    #si es cambia el datagrama canviar 3 id a identifier
    # ----------------- END OF FUNCTION --------------------- #


def create_similarity_graph(artist_audio_features_df: pd.DataFrame, similarity: str, out_filename: str = None) -> \
        nx.Graph:
    """
    Create a similarity graph from a dataframe with mean audio features per artist.

    :param artist_audio_features_df: dataframe with mean audio features per artist.
    :param similarity: the name of the similarity metric to use (e.g. "cosine" or "euclidean").
    :param out_filename: name of the file that will be saved.
    :return: a networkx graph with the similarity between artists as edge weights.
    """
    # ------- IMPLEMENT HERE THE BODY OF THE FUNCTION ------- #
    graf = nx.Graph()
    for fila1 in artist_audio_features_df.itertuples(index=False):
        id1 = fila1[0]
        if not graf.has_node(id1):
            graf.add_node(id1)
        for fila2 in artist_audio_features_df.itertuples(index=False):
            id2 = fila2[0]

            if not graf.has_node(id2):
                graf.add_node(id2)
            if id1!= id2 and not graf.has_edge(id1, id2):

                if similarity == 'euclidian':
                    distancia_euclidiana = 1/(1+euclidean(fila1[2:],fila2[2:]))
                    graf.add_edge(id1,id2, weight = distancia_euclidiana)
                elif similarity == 'cosine':
                    cosinus = 1 - np.dot(fila1[2:], fila2[2:]) / (np.linalg.norm(fila1[2:]) * np.linalg.norm(fila2[2:]))
                    graf.add_edge(id1, id2, weight = 1 / (1 + cosinus))
    nx.write_graphml(graf, out_filename)
    return graf
    # ----------------- END OF FUNCTION --------------------- #


if __name__ == "__main__":
    # ------- IMPLEMENT HERE THE MAIN FOR THIS SESSION ------- #
    gB = nx.read_graphml('gB.graphml')
    gD = nx.read_graphml('gD.graphml')
    D = pd.read_csv('D.csv')
    g_b = retrieve_bidirectional_edges(gB,'g\'b.graphml')
    g_d = retrieve_bidirectional_edges(gD,'g\'d.graphml')
    af= compute_mean_audio_features(D)
    cs = create_similarity_graph(af,'euclidian','similarity graph')
    prune_low_weight_edges(g = cs, min_percentile = (100 - (g_b.size()*100 / cs.size())), out_filename = 'gwB.graphml')
    gwB = nx.read_graphml('gwB.graphml')
    prune_low_weight_edges(g = cs, min_percentile =  (100 - (g_d.size()*100 / cs.size())), out_filename = 'gwD.graphml')
    gwD = nx.read_graphml('gwD.graphml')

    print('\n Order and size of the graphs:\n')
    print('g\'b Order:',g_b.order(),'g\'b Size:', g_b.size())
    print('g\'d Order:', g_d.order(), 'g\'d Size:', g_d.size())
    print('gwB Order:', gwB.order(), 'gwB Size:', gwB.size())
    print('gwD Order:', gwD.order(), 'gwD Size:', gwD.size())

    print('\n Number of strong components:\n')
    print('Graf gB:',nx.number_strongly_connected_components(gB))
    print('Graf gD:', nx.number_strongly_connected_components(gD))

    print('\n Number of weak components:\n')
    print('Graf gB:', nx.number_weakly_connected_components(gB))
    print('Graf gD:', nx.number_weakly_connected_components(gD))

    print('\n Number of components:\n')
    print('Graf g\'B:', nx.number_connected_components(g_b))
    print('Graf g\'D:', nx.number_connected_components(g_d))

    print('\n Size of the largest component:\n')
    print('Mida del component més gran a gwB:', len(max(nx.connected_components(g_b), key=len)))
    print('Mida del component més gran a gwD:', len(max(nx.connected_components(g_d), key=len)))

    # ------------------- END OF MAIN ------------------------ #
