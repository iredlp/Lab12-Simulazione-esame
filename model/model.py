import networkx as nx
from database.DAO import DAO

class Model:
    def __init__(self):
        self._graph = nx.Graph()  # grafo semplice
        self._idMapAttori = {}

    def getAllVoti(self):
        self._voti=DAO.getAllRange()
        return self._voti

    def buildGraph(self, voto1, voto2):
        # svuoto il grafo
        self._graph.clear()

        self._attori = DAO.getAllNodes(voto1,voto2)

        for a in self._attori:
            self._idMapAttori[a.id] = a

        # aggiungo i nodi al grafo
        self._graph.add_nodes_from(self._attori)

       # edges = DAO.getAllEdges(genere, self._idMapArtisti)
        # for e in edges:
        # self._graph.add_edge(e.a1, e.a2)

        # for n in self._generi:
        # self.mappaArtisti[n.ArtistId] = n
        # self._archi = DAO.getEdges(genere)
        #._pop = DAO.getPop(genere)
        # Iteriamo direttamente sugli oggetti Arco restituiti dal DAO
       # for edge in edges:
          #  u = edge.a1  # Questo è l'oggetto Artista 1
          #  v = edge.a2  # Questo è l'oggetto Artista 2

            # Recuperiamo la popolarità usando gli ID numerici degli artisti
            #up = self._pop.get(u.ArtistId, 0)
           # vp = self._pop.get(v.ArtistId, 0)

            # Calcoliamo il peso totale
           # peso_arco = up + vp

            # Gestione del verso basata sulla popolarità
            #if up < vp:
                # Nota: u e v sono già oggetti Artista, li passiamo direttamente a NetworkX!
               # self._graph.add_edge(u, v, weight=peso_arco)
            #elif up > vp:
              #  self._graph.add_edge(v, u, weight=peso_arco)
           # else:
              #  self._graph.add_edge(u, v, weight=peso_arco)
               # self._graph.add_edge(v, u, weight=peso_arco)

    def getAllNodes(self):
        return list(self._graph.nodes())

    def getGraphDetails(self):
        return len(self._graph.nodes), len(self._graph.edges)
