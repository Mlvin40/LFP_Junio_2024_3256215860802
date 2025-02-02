from tkinter import PhotoImage, Label
from PIL import Image, ImageTk
from Backend.Lexer import Lexer
from graphviz import Digraph

class Grafo:
    def __init__(self):
        self.lexer = Lexer()
        self.imagenes_procesadas = []
        self.PATH_IMAGEN = 'Grafos/imgGrafo'

    # Este metodo se encarga de devolver una lista de todas las imagenes encontradas en el archivo de entrada
    def escanear_tokens(self, contenido):
        
        ##################################################################
        """esto se hace para limpiar la lista de imagenes procesadas
        en caso de que se vuelva a analizar un nuevo archivo de entrada"""
        self.imagenes_procesadas = []
        self.lexer.reiniciar_listas()
        ##################################################################
        
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
    
    #con este metodo se extraen todas las conexiones existentes en el archivo de entrada
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

    #En base al numero de opcion seleccionada en el combobox se mostrara el grafo correspondiente
    def mostrar_grafo(self, posicion, label):
                    
        imagen = self.imagenes_procesadas[posicion]
        dot = Digraph(comment="LENGUAJES FORMALES Y DE PROGRAMACIÓN") 
    
        dot.attr(dpi = '300') # Calidad de la imagen generada (grafo)
        dot.attr(label=imagen["nombre"].strip("'") , labelloc="t", fontsize ="20") #Se agrega el nombre del grafo en un label
        
        #Con este bucle se agregan los nodos al grafo
        for nodo in imagen["nodos"]:
            dot.node(nodo[0], nodo[1])
            
        #Con este bucle se agregan las conexiones al grafo
        for conexion in imagen["conexiones"]:
            dot.edge(conexion[0], conexion[1])
            
        #Renderizamos el grafo
        dot.render(self.PATH_IMAGEN, format='png', view=False)
        
        #Muestra la imagen en el label de la interfaz grafica
        #################################################################################
        imagen_grafo = Image.open(self.PATH_IMAGEN+'.png')
        imagen_grafo = imagen_grafo.resize((label.winfo_width(), label.winfo_height())) # Redimensionar la imagen
        imagen_grafo = ImageTk.PhotoImage(imagen_grafo)#parsear la imagen al formato del label
        label.configure(image=imagen_grafo)#Se agrega la imagen parseada al label
        label.image = imagen_grafo 
        #################################################################################
        
            

