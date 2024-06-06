import networkx as nx
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import numpy as np


# ------- IMPLEMENT HERE ANY AUXILIARY FUNCTIONS NEEDED ------- #
CLIENT_ID = "clientID"
CLIENT_SECRET = "clientSecret"
auth_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(auth_manager=auth_manager)
playlists = sp.user_playlists('spotify')
"""while playlists:
    for i , playlist in enumerate(playlists['items']):
        print ("%4d %s %s"%(i + 1 + playlists['offset'], playlist['uri'], playlist['name']) )
    if playlists ['next']:
        playlists = sp.next(playlists)
    else:
        playlists = None"""


# --------------- END OF AUXILIARY FUNCTIONS ------------------ #


def search_artist(sp: spotipy.client.Spotify, artist_name: str) -> str:
    """
    Search for an artist in Spotify.

    :param sp: spotipy client object
    :param artist_name: name to search for.
    :return: spotify artist id.
    """
    # ------- IMPLEMENT HERE THE BODY OF THE FUNCTION ------- #
    """Busco pel nom de l'artista i retorno la id."""
    results = sp.search(q='artist:' + artist_name, type='artist')
    return results['artists']['items'][0]['id']
    # ----------------- END OF FUNCTION --------------------- #


def crawler(sp: spotipy.client.Spotify, seed: str, max_nodes_to_crawl: int, strategy: str = "BFS",
            out_filename: str = "g.graphml") -> nx.DiGraph:
    """
    Crawl the Spotify artist graph, following related artists.

    :param sp: spotipy client object
    :param seed: starting artist id.
    :param max_nodes_to_crawl: maximum number of nodes to crawl.
    :param strategy: BFS or DFS.
    :param out_filename: name of the graphml output file.
    :return: networkx directed graph.
    """
    # ------- IMPLEMENT HERE THE BODY OF THE FUNCTION ------- #

    """La diferència principal entre els dos mètodes es com tractem llista a visitar, si com una llista o una pila, per a DFS
    com una pila i ens quedem l'ultim valor afegit a la pila. Per BFS com una llista/cua i vaig agafant valors en ordre.
    Amb pop(0) agafo el primer valor de la llista i el borro(BFS). Per DFS a més cal girar al afegir els valors de la llista per explorar pel primer veí"""

    if strategy=="BFS":
        id_artista = seed
        """Afegeix-ho el primer node."""
        artista = sp.artist(id_artista)
        llista_visitar = [artista]
        nodes = sp.artist_related_artists(id_artista)
        graf = nx.DiGraph()
        comptador = 0
        visitats = []
        """Afegeix-ho els 20 primers veïns a una llista a visitar i a la llista visitats."""
        for node in nodes['artists']:  # RECORRO LA TOTS ELS POSSIBLES NODES I ELS AFEGEIX-HO A UNA LLISTA A VISITAR
            llista_visitar.append(node)
            visitats.append(node['id'])
        """Mentres la llista a visitar no estigui buida, fes un pop del primer element"""
        while llista_visitar:
            artista = llista_visitar.pop(0)
            nom = artista['name']
            artist_id = artista['id']
            followers = artista['followers']['total']
            popularity = artista['popularity']
            genres = artista['genres']
            """Fem un comptador que iterararà fins que s'arribi al node màxim."""
            if comptador < max_nodes_to_crawl:
                comptador += 1
                """Obtinc els veïns del node actual i els afegeix-ho a la llista a vistiar si no estan visitats."""
                nodes = sp.artist_related_artists(artist_id)
                for node in nodes['artists']:
                    if node['id'] not in visitats:
                        llista_visitar.append(node)
                        visitats.append(node['id'])
            """Afegeix-ho com a valor del node un string (és una llista) amb tots els valors que s'han de guardar."""
            if not graf.has_node(artist_id):
                node_attributes = {'nom': nom, 'followers': followers, 'popularity': popularity,
                                   'genres': ', '.join(map(str, genres))}
                graf.add_node(artist_id, **node_attributes)
            """Afegeix-ho les arestes al graf tantes vegades fins arribar al màxim."""
            if comptador < max_nodes_to_crawl:
                for node1 in nodes['artists']:
                    if not graf.has_node(node1['id']):
                        nom = node1['name']
                        artist_id = node1['id']
                        followers = node1['followers']['total']
                        popularity = node1['popularity']
                        genres = node1['genres']
                        node_attributes = {'nom': nom, 'followers': followers, 'popularity': popularity,
                                           'genres': ', '.join(map(str, genres))}
                        graf.add_node(node1['id'], **node_attributes)
                    graf.add_edge(artist_id, node1['id'])


    elif strategy=="DFS":

        id_artista = seed
        """Carrego la informació del primer node."""
        artista = sp.artist(id_artista)
        llista_visitar = [artista]
        nodes = sp.artist_related_artists(id_artista)
        graf = nx.DiGraph()
        comptador = 0
        visitats = []
        """Afegeix-ho els 20 primers veïns a una llista a visitar i a la llista visitats."""
        for node in nodes['artists'][
                    ::-1]:  # RECORRO LA TOTS ELS POSSIBLES NODES I ELS AFEGEIX-HO A UNA LLISTA A VISITAR INVERSAMENT PER FER DFS
            llista_visitar.append(node)

        while llista_visitar:
            artista = llista_visitar.pop()
            nom = artista['name']
            artist_id = artista['id']
            followers = artista['followers']['total']
            popularity = artista['popularity']
            genres = artista['genres']
            """Afegeix-ho com a valor del node un string (és una llista) amb tots els valors que s'han de guardar."""
            if not graf.has_node(artist_id):
                node_attributes = {'nom': nom, 'followers': followers, 'popularity': popularity,'genres':', '.join(map(str, genres))}
                graf.add_node(artist_id, **node_attributes)
                #graf.add_node(artista['id'], name=artista['name'], id=artista['id'], followers=artista['followers']['total'],popularitat=artista['popularity'], generes=str(artista['genres']))
            """Fem un comptador que iterararà fins que s'arribi al node màxim."""
            if comptador < max_nodes_to_crawl:
                comptador += 1
                """Obtinc els veïns del node actual i els afegeix-ho a la llista a visitar si no estan visitats."""
                nodes = sp.artist_related_artists(artist_id)
                for node in nodes['artists'][::-1]:
                    if node['id'] not in visitats:
                        llista_visitar.append(node)
            visitats.append(artist_id)
            """Afegeix-ho les arestes al graf tantes vegades fins arribar al màxim."""
            if comptador < max_nodes_to_crawl:
                for node1 in nodes['artists']:
                    if not graf.has_node(node1['id']):
                        nom = node1['name']
                        artist_id = node1['id']
                        followers = node1['followers']['total']
                        popularity = node1['popularity']
                        genres = node1['genres']
                        node_attributes = {'nom': nom, 'followers': followers, 'popularity': popularity,
                                           'genres': ', '.join(map(str, genres))}
                        graf.add_node(node1['id'], **node_attributes)
                    graf.add_edge(artist_id, node1['id'])





    else:
        print("ERROR: BFS O DFS MAL INTRODUÏT")


    # node append dicc_artist = name, artist_id, followers, popularity, genres
    """Instrucció per guardar el graf com a grafhml"""
    nx.write_graphml(graf,out_filename)
    return graf
    # ----------------- END OF FUNCTION --------------------- #


def get_track_data(sp: spotipy.client.Spotify, graphs: list, out_filename: str) -> pd.DataFrame:
    """
    Get track data for each visited artist in the graph.

    :param sp: spotipy client object
    :param graphs: a list of graphs with artists as nodes.
    :param out_filename: name of the csv output file.
    :return: pandas dataframe with track data.
    """
    # ------- IMPLEMENT HERE THE BODY OF THE FUNCTION ------- #
    track_data_llista = []  # Llista de llistes amb la informació de les pistes
    explorats = []  # Llista dels artistes explorats

    for graf in graphs:
        for node, data in graf.nodes(data = True):
            artist_id = node
            if artist_id not in explorats and graf.out_degree(node) > 0:
                explorats.append(artist_id)

                # Obtenim les top tracks de l'artista
                tt = sp.artist_top_tracks(artist_id, country='ES')

                # Obtenim els ids de les top tracks per una sola crida
                track_ids = [track['id'] for track in tt['tracks']]

                # Obtenim les característiques d'àudio de les top tracks
                audio_features = sp.audio_features(track_ids)

                for i, track in enumerate(tt['tracks']):
                    tt_a = [track['id'], track['duration_ms'], track['name'], track['popularity']]
                    tt_b = [track['album']['id'], track['album']['name'], track['album']['release_date']]
                    tt_c = [artist_id, data['nom']]

                    aa_a = [audio_features[i]['danceability'], audio_features[i]['energy'],
                            audio_features[i]['loudness'], audio_features[i]['speechiness'],
                            audio_features[i]['acousticness'], audio_features[i]['instrumentalness'],
                            audio_features[i]['liveness'], audio_features[i]['valence'],
                            audio_features[i]['tempo']]

                    # Afegim la informació de la pista a la llista
                    track_data_llista.append(tt_a + aa_a + tt_b + tt_c)

    dataframe = pd.DataFrame(track_data_llista, columns=['song_identifier', 'song_duration', 'song_name',
                                                             'song_popularity', 'audio_danceability', 'audio_energy',
                                                             'audio_loudness', 'audio_speechiness',
                                                             'audio_acousticness',
                                                             'audio_instrumentalness', 'audio_liveness',
                                                             'audio_valence',
                                                             'audio_tempo', 'album_identifier', 'album_name',
                                                             'album_release_date', 'artist_identifier', 'artist_name'])

    # Guardem el DataFrame en un fitxer CSV
    return dataframe.to_csv(str(out_filename), index=False)


#if __name__ == "_main_":
# ------- IMPLEMENT HERE THE MAIN FOR THIS SESSION ------- #

a = search_artist(sp,'Taylor Swift')
print(a)
a2 = search_artist(sp,'Hippo Campus')
print(a2)
gD = crawler(sp,a,100,'DFS','gD.graphml')
gB = crawler(sp, a, 100, 'BFS', 'gB.graphml')
D=get_track_data(sp,[gD,gB],'D')

print("Ordre del graf gD:",gD.order())
print("Ordre del graf gB:",gB.order())
print("Mida del graf gD:",gD.size())
print("Mida del graf gB:",gB.size())

"""Codi que calcula el mínim, màxim i la mediana, ho fem calculant el diccionari dels graus d'entrada i sortida i fent els càlculs pertinents
Calculant el màxim i mínim del diccionari. Per calcular la mediana utilitzem la centralitat de grau del node."""

in_degrees_gB = dict(gB.in_degree())
out_degrees_gB = dict(gB.out_degree())

in_degrees_gD = dict(gD.in_degree())
out_degrees_gD = dict(gD.out_degree())

print("Valors mínim, màxim i mediana del grau d'entrada de gB")
min_in_degree_gB = min(in_degrees_gB.values())
max_in_degree_gB = max(in_degrees_gB.values())
median_in_degree_gB = np.median(list(in_degrees_gB.values()))
print(min_in_degree_gB)
print(max_in_degree_gB)
print(median_in_degree_gB)

print("Valors mínim, màxim i mediana del grau de sortida de gB")
min_out_degree_gB = min(out_degrees_gB.values())
max_out_degree_gB = max(out_degrees_gB.values())
median_out_degree_gB = np.median(list(out_degrees_gB.values()))
print(min_out_degree_gB)
print(max_out_degree_gB)
print(median_out_degree_gB)

print("Valors mínim, màxim i mediana del grau d'entrada de gD")
min_in_degree_gD = min(in_degrees_gD.values())
max_in_degree_gD = max(in_degrees_gD.values())
median_in_degree_gD = np.median(list(in_degrees_gD.values()))
print(min_in_degree_gD)
print(max_in_degree_gD)
print(median_in_degree_gD)

print("Valors mínim, màxim i mediana del grau de sortida de gD")
min_out_degree_gD = min(out_degrees_gD.values())
max_out_degree_gD = max(out_degrees_gD.values())
median_in_degree_gD = np.median(list(out_degrees_gD.values()))
print(min_out_degree_gD)
print(max_out_degree_gD)
print(median_in_degree_gD)

# ------------------- END OF MAIN ------------------------ #
a = search_artist(sp,'Taylor Swift')
gD = crawler(sp,a,100,'DFS','gD.graphml')
gB = crawler(sp, a, 100, 'BFS', 'gB.graphml')
D=get_track_data(sp,[gD,gB],'D')

print("Ordre del graf gD:",gD.order())
print("Ordre del graf gB:",gB.order())
print("Mida del graf gD:",gD.size())
print("Mida del graf gB:",gB.size())

"""Codi que calcula el mínim, màxim i la mediana, ho fem calculant el diccionari dels graus d'entrada i sortida i fent els càlculs pertinents
Calculant el màxim i mínim del diccionari. Per calcular la mediana utilitzem la centralitat de grau del node."""

in_degrees_gB = dict(gB.in_degree())
out_degrees_gB = dict(gB.out_degree())

in_degrees_gD = dict(gD.in_degree())
out_degrees_gD = dict(gD.out_degree())

print("Valors mínim, màxim i mediana del grau d'entrada de gB")
min_in_degree_gB = min(in_degrees_gB.values())
max_in_degree_gB = max(in_degrees_gB.values())
median_in_degree_gB = np.median(list(in_degrees_gB.values()))
print(min_in_degree_gB)
print(max_in_degree_gB)
print(median_in_degree_gB)

print("Valors mínim, màxim i mediana del grau de sortida de gB")
min_out_degree_gB = min(out_degrees_gB.values())
max_out_degree_gB = max(out_degrees_gB.values())
median_out_degree_gB = np.median(list(out_degrees_gB.values()))
print(min_out_degree_gB)
print(max_out_degree_gB)
print(median_out_degree_gB)

print("Valors mínim, màxim i mediana del grau d'entrada de gD")
min_in_degree_gD = min(in_degrees_gD.values())
max_in_degree_gD = max(in_degrees_gD.values())
median_in_degree_gD = np.median(list(in_degrees_gD.values()))
print(min_in_degree_gD)
print(max_in_degree_gD)
print(median_in_degree_gD)

print("Valors mínim, màxim i mediana del grau de sortida de gD")
min_out_degree_gD = min(out_degrees_gD.values())
max_out_degree_gD = max(out_degrees_gD.values())
median_in_degree_gD = np.median(list(out_degrees_gD.values()))
print(min_out_degree_gD)
print(max_out_degree_gD)
print(median_in_degree_gD)