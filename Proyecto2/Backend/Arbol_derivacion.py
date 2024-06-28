from graphviz import Digraph

class ArbolDeDerivacion:
    def __init__(self):
        self.dot = Digraph(comment='Árbol de Derivación')
        self.node_count = 0

    def agregar_nodo(self, etiqueta):
        node_id = f'node{self.node_count}'
        self.dot.node(node_id, etiqueta)
        self.node_count += 1
        return node_id
    
    def agregar_conexion(self, nodo_padre, nodo_hijo):
        self.dot.edge(nodo_padre, nodo_hijo)

    def guardar_arbol(self, nombre_archivo):
        self.dot.render(nombre_archivo, format = 'svg')
