import itertools

import networkx as nx

from database.DAO import DAO


class Model:

    def __init__(self):
        self._graph = nx.Graph()
        self._allNodes = []
        self._idMapPiloti = {}

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


