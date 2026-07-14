import networkx as nx
from database.DAO import DAO

class Model:
    def __init__(self):
        self._graph = nx.Graph()  # grafo semplice
        self._idMapAttori = {}

    def get_cammino_massimo(self):
        self._best_path = []

        # Valutiamo ogni nodo del grafo come potenziale partenza
        for nodo_partenza in self._graph.nodes():
            # Inizializziamo il cammino corrente con il nodo di partenza
            self._ricorsione([nodo_partenza])

        return self._best_path

    def _ricorsione(self, parziale):
        nodo_corrente = parziale[-1]
        # Esploriamo i vicini del nodo corrente
        vicini = self._graph.neighbors(nodo_corrente)
        ha_successori_validi = False

        for vicino in vicini:
            # Vincolo 1: Il cammino deve essere SEMPLICE (nessun nodo ripetuto)
            if vicino not in parziale:
                # Vincolo 2: L'età deve essere strettamente DECRESCENTE
                # Significa che l'attore successivo deve essere più GIOVANE,
                # quindi la sua date_of_birth deve essere MAGGIORE (più recente)
                if vicino.date_of_birth > nodo_corrente.date_of_birth:
                    ha_successori_validi = True
                    parziale.append(vicino)
                    self._ricorsione(parziale)
                    parziale.pop()  # Backtracking

        # Caso terminale spontaneo: se non ci sono vicini validi che rispettano il vincolo,
        # controlliamo se il cammino parziale attuale è il più lungo trovato finora.
        if not ha_successori_validi:
            # Valutiamo la lunghezza in termini di numero di archi (nodi - 1) o numero di nodi?
            # Solitamente nei grafi la lunghezza è il numero di ARCHI.
            if len(parziale) > len(self._best_path):
                self._best_path = list(parziale)

    def getAllVoti(self):
        self._voti=DAO.getAllRange()
        return self._voti

    def buildGraph(self, voto1, voto2):
        # svuoto il grafo
        self._graph.clear()
        self._idMapAttori = {}

        self._attori = DAO.getAllNodes(voto1,voto2)

        for a in self._attori:
            if a.date_of_birth is not None:
                self._idMapAttori[a.id] = a
                self._graph.add_node(a)
        #self._graph.add_nodes_from(self._attori)

        # 3. Estraggo gli archi dal DB (senza filtri di range, se passiamo tramite idMap)
        # Se invece il tuo DAO si aspetta ancora i voti, lascia DAO.getAllEdges(voto1, voto2)
        edges = DAO.getAllEdges(voto1,voto2)
        for e in edges:
            # Recuperiamo gli ID (assumendo che il DAO restituisca un dizionario con chiavi 'id1' e 'id2')
            id1 =e.a1 # e['a1']
            id2 =e.a2 #e['a2']
            incasso_str=e.peso
            # Gestione dell'incasso (stringa -> intero)
            if incasso_str and '$' in incasso_str:
                peso = int(incasso_str.replace('$', '').replace(' ', '').strip())
            else:
                peso = 0  # Ignoriamo le rupie indiane e i valori nulli

            # 4. CONTROLLO FONDAMENTALE: l'arco esiste solo se entrambi gli attori
            # sono nella nostra idMap (cioè sono nel range di voti e hanno un'età valida)
            if id1 in self._idMapAttori and id2 in self._idMapAttori:
                attore1 = self._idMapAttori[id1]
                attore2 = self._idMapAttori[id2]

                # Se i due attori hanno fatto più film insieme, sommiamo il peso
                #if self._graph.has_edge(attore1, attore2):
                  #  self._graph[attore1][attore2]['weight'] += peso
               # else:
                self._graph.add_edge(attore1, attore2, weight=peso)


    def getAllNodes(self):
        return list(self._graph.nodes())

    def getGraphDetails(self):
        return len(self._graph.nodes), len(self._graph.edges)

    def getTop5Archi(self):
        return sorted(self._graph.edges(data=True),
                      key=lambda x: x[2]["weight"], reverse=True)[:5]

    def getConnessaInfo(self):
        componets=list(nx.connected_components(self._graph)) #PRENDO LE COMPONENTI CONNESSE
        #NUMERO COMPONENTI CONNESSE
        #num_components = len(componets)
        #la più grande
        largest=max(componets, key= len) #indico su quale funzione basarsi
        #uso un sottografo
        subgraph=self._graph.subgraph(largest).copy()
        orederedNodes=sorted(subgraph.nodes(), key=lambda n:self._graph.degree(n), reverse=True)

       # details=[(n, self._graph.degree(n)) for n in orederedNodes]

        return len(componets), largest
