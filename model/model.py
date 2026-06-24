import copy
import itertools

import networkx as nx

from database.DAO import DAO


class Model:

    def __init__(self):
        self._graph = nx.Graph()
        self._allNodes = []
        self._idMapPiloti = {}
        self._optListPiloti = None
        self._minDistAnni = None

    def getListaPilotiOttima(self, k):
        self._optListPiloti = []
        self._minDistAnni = 100*365   #parto da un valore in giorni alto poiche devo minimizzare

        components = list(nx.connected_components(self._graph))

        if len(components) < k:
            #allora non ho abbastanza componenti connesse da cui pescare, e non posso trovare una sol
            return None, 0

        parziale = []
        self._ricorsione(components, k, parziale, 0)
        return self._optListPiloti, self._minDistAnni

    def _ricorsione(self, components, k, parziale, indexComponente):
        #condizione di ottimalità
        if len(parziale) == k:
            #ho una soluzione accettabile.
            dateDiNascita = [p.dob for p in parziale]
            diffEtaPiloti = (max(dateDiNascita) - min(dateDiNascita)).days
            if diffEtaPiloti < self._minDistAnni:
                self._optListPiloti = copy.deepcopy(parziale)
                self._minDistAnni = diffEtaPiloti

        #condizione terminale
        #1) finisco le componenti da cui pescare (mi baso sull'indice)
        #2) se non ho abbastanza componenti rimanenti per arrivare a k piloti in parziale
        if indexComponente >= len(components) or (len(components) - indexComponente) < (k - len(parziale)):
            return

        #se non sono uscito, allora posso ancora aggiungere piloti. Per questa componente
        #provo ad ingaggiare un pilota oppure a non ingaggiare nessuno

        #caso1, inserisco un pilota di questa comp connessa. Qua provo tutti i piloti che fanno
        #parte della comp connessa in esame
        componente = components[indexComponente]
        for pilota in componente:
            parziale.append(pilota)
            self._ricorsione(components, k, parziale, indexComponente+1)
            parziale.pop()

        #caso2, mi tengo un branch di esplorazioni in cui non ho preso proprio nessuno
        #da questa componente
        self._ricorsione(components, k, parziale, indexComponente+1)




    def buildGraph(self, anno1, anno2):
        self._graph.clear()
        self._graph.clear_edges()
        self._idMapPiloti.clear()

        self._allNodes = DAO.getAllNodes(anno1, anno2)
        for p in self._allNodes:
            self._idMapPiloti[p.driverId] = p

        self._graph.add_nodes_from(self._allNodes)
        self.addEdges(anno1, anno2)

    def addEdges(self, anno1, anno2):
        listaArchi, listaIdPiloti = DAO.getAllEdges(anno1, anno2)

        listaAggiunti = []
        for tupla in listaIdPiloti:
            if tupla[0] in self._idMapPiloti.keys() and tupla[1] in self._idMapPiloti.keys():
                if (tupla[1], tupla[0]) in listaAggiunti:
                    continue
                else:
                    p1 = self._idMapPiloti[tupla[0]]
                    p2 = self._idMapPiloti[tupla[1]]
                    peso = self.getPeso(tupla[0], tupla[1], listaArchi)
                    self._graph.add_edge(p1, p2, weight=peso)
                    listaAggiunti.append((tupla[0], tupla[1]))

    def getPeso(self, id1, id2, listaArchi):
        for tupla in listaArchi:
            if tupla[0] == id1 and tupla[1] == id2:
                return tupla[2]
        return None

    def getTop3(self):
        lista = self._graph.edges(data=True)

        #for a in lista:
           # print(a)

        result = sorted(lista, key=lambda x: x[2]['weight'], reverse=True)
        return result[:3]

    def getNumCompConn(self):
        return nx.number_connected_components(self._graph)

    def getCompConn(self):
        lista = nx.connected_components(self._graph)
        max = 0
        comp = None
        for e in lista:
            if len(e) > max:
                max = len(e)
                comp = e
        result = self.getOrdineComp(comp)
        return max, comp, result

    def getOrdineComp(self, comp):
        lista = []
        for pilota in comp:
            grado = self._graph.degree(pilota)
            print(grado)
            lista.append((pilota, grado))
        lista.sort(key=lambda x: x[1], reverse=True)
        return lista







    def getNumNodi(self):
        return len(self._graph.nodes)

    def getNumArchi(self):
        return len(self._graph.edges)

    def getAllYears(self):
        return DAO.getAllYears()


