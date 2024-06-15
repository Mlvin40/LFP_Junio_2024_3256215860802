import sys
import os

# Añadir el directorio raíz del proyecto al sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Backend.Lexer import Lexer
from graphviz import Digraph


class Grafo:
    def __init__(self):
        self.lexer = Lexer()
        self.imagenes_procesadas = []

    # Este metodo se encarga de devolver una lista de todas las imagenes encontradas en el archivo de entrada
    def escanear_tokens(self, contenido):
        self.lexer.analizar(contenido)
        imagenes_procesadas = []

        for tokens in self.lexer.lista_imagenes:
            nombre = self.extraer_nombre(tokens)
            nodos = self.extraer_nodos(tokens)
            conexiones = self.extraer_conexiones(tokens)
            imagenes_procesadas.append({
                "nombre": nombre,
                "nodos": nodos,
                "conexiones": conexiones
            })
        
        self.imagenes_procesadas = imagenes_procesadas
    
    def extraer_nombre(self, tokens):
        return tokens[2].lexema
    
    # Este metodo se encarga de extraer todos los nodos existentes en el archivo de entrada
    def extraer_nodos(self, tokens):
        NODOS = []
        i = 0
        
        # Recorre la lista de tokens
        while i < len(tokens):
            if tokens[i].nombre == 'Palabra Reservada' and tokens[i].lexema == 'nodos':
                i += 3  # Saltar "nodos -> ["
                while i < len(tokens) and (tokens[i].nombre != 'Símbolo' or tokens[i].lexema != ']'):
                    if tokens[i].nombre == 'String' and tokens[i + 1].nombre == 'Símbolo' and tokens[i + 1].lexema == ':' and tokens[i + 2].nombre == 'String':
                        nombre_nodo = tokens[i].lexema.strip("'")
                        texto_nodo = tokens[i + 2].lexema.strip("'")
                        NODOS.append([nombre_nodo, texto_nodo])
                        i += 3  # para saltar la sintaxis 'nombre_nodo': 'texto_nodo'
                    elif tokens[i].lexema == ',':
                        i += 1  # Saltar la coma
                    else:
                        i += 1
            else:
                i += 1
        return NODOS

    def extraer_conexiones(self, tokens):
        CONEXIONES = []

        i = 0
        while i < len(tokens):
            if tokens[i].nombre == 'Palabra Reservada' and tokens[i].lexema == 'conexiones':
                i += 3  # Saltar "conexiones -> ["
                while i < len(tokens) and (tokens[i].nombre != 'Símbolo' or tokens[i].lexema != ']'):
                    if tokens[i].nombre == 'Símbolo' and tokens[i].lexema == '{':
                        i += 1  # Saltar '{'
                        if tokens[i].nombre == 'String' and tokens[i + 1].nombre == 'Símbolo' and tokens[i + 2].nombre == 'String':
                            nombre_nodo1 = tokens[i].lexema.strip("'")
                            nombre_nodo2 = tokens[i + 2].lexema.strip("'")
                            CONEXIONES.append([nombre_nodo1, nombre_nodo2])
                            i += 4  # para saltar la sintaxis 'nombre_nodo1' > 'nombre_nodo2' y saltar '}'
                        elif tokens[i].lexema == ',':
                            i += 1  # Saltar la coma
                        else:
                            i += 1
                    else:
                        i += 1
            else:
                i += 1
                
        return CONEXIONES

    def mostrar_grafo(self, posicion):
        """if posicion < 0 or posicion >= len(self.imagenes_procesadas):
            print(f"No hay imagen en la posición {posicion}")
            return"""
            
        imagen = self.imagenes_procesadas[posicion]
        dot = Digraph(comment="Grafo") 
        dot.attr(rankdir='LR')  # Establece la dirección de las conexiones
        label=imagen["nombre"]
        
        
        dot.attr(label=f'"{imagen["nombre"]}"') #Se agrega el nombre del grafo en un label
        
        #Con este bucle se agregan los nodos al grafo
        for nodo in imagen["nodos"]:
            dot.node(nodo[0], nodo[1])
            
        #Con este bucle se agregan las conexiones al grafo
        for conexion in imagen["conexiones"]:
            dot.edge(conexion[0], conexion[1])
        
        # Renderizamos el grafo
        dot.render(f'imagen{posicion + 1}', format='png', view=True)
    

# Ejemplo de uso
contenido_prueba = """
nombre -> 'El mejor grafo';
nodos -> [
'nombre_nodo1': 'texto_nodo1',
'nombre_nodo2': 'texto nodo2',
'nombre_nodo3': 'texto_nodo3'
];
conexiones ->[
{'nombre_nodo1' > 'nombre_nodo2'},
{'nombre_nodo3' > 'nombre_nodo2'}
]
"""

grafo = Grafo()
grafo.escanear_tokens(contenido_prueba)

for idx, imagen in enumerate(grafo.imagenes_procesadas):
    print(f"Imagen {idx + 1}:")
    print("Nombre:", imagen["nombre"])
    print("Nodos:")
    for nodo in imagen["nodos"]:
        print(list(nodo))  # Imprime cada nodo como una lista 
    print("Conexiones:")
    for conexion in imagen["conexiones"]:
        print(list(conexion))  # Imprime cada conexión como una lista 
    print()

grafo.mostrar_grafo(0)

