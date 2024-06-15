import sys
import os

# Añadir el directorio raíz del proyecto al sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Definición de la clase Token
class Token:
    def __init__(self, nombre, lexema, linea, columna):
        self.nombre = nombre
        self.lexema = lexema
        self.linea = linea
        self.columna = columna

    def __repr__(self):
        return f"Token({self.nombre}, {self.lexema}, {self.linea}, {self.columna})"

# Definición de la clase TokenError (si es necesario)
class TokenError:
    def __init__(self, tipo, lexema, linea, columna):
        self.tipo = tipo
        self.lexema = lexema
        self.linea = linea
        self.columna = columna

    def __repr__(self):
        return f"TokenError({self.tipo}, {self.lexema}, {self.linea}, {self.columna})"

# Clase para analizar el código fuente y generar tokens
class Lexer:
    def __init__(self) -> None:
        self.entrada = ""
        self.keywords = {'nombre', 'nodos', 'conexiones'}
        
        self.lista_imagenes = []
        
        self.tokens = []  # Lista para almacenar tokens válidos
        self.errores = []  # Lista para almacenar errores léxicos
        
        self.ERROR_LEXICO = "Identificador Desconocido"
        self.SIMBOLO = "Símbolo"
        self.PALABRA_RESERVADA = "Palabra Reservada"
        self.FLECHA = "Flecha"
        self.STRING = "String"
        self.SEPARADOR = "Separador"
        
        # verifica si existe más de una imagen
        self.haySeparador = False
        
    def isCaracterValido(self, caracter):
        return caracter in [';', '[', ']', ':', ',', '{', '}', '>']
    
    def esPunto(self, caracter):
        return caracter == '.'
    
    def analizar(self, entrada):
        # guarda la entrada de texto en la variable entrada para poder analizarla
        self.entrada = entrada
        
        linea = 1
        columna = 1
        lexema = ""
        estado = 0
        
        for caracter in self.entrada:
            # mantiene la columna en la que se encuentra el lexema actual
            columna_actual = columna - len(lexema)
            if estado == 0:
                if caracter.isalpha():
                    lexema += caracter
                    estado = 1
                    
                elif caracter == "-":
                    lexema += caracter
                    estado = 2
                    
                elif caracter == "'":
                    lexema += caracter
                    estado = 3
                    
                elif self.isCaracterValido(caracter):
                    lexema += caracter
                    self.tokens.append(Token(self.SIMBOLO, lexema, linea, columna_actual))
                    lexema = ""
                    
                elif caracter == '.':
                    lexema += caracter
                    estado = 5
                    
                elif caracter.isspace():
                    if caracter == '\n':  # si el caracter es un salto de línea se aumenta el contador de líneas y se reinicia el contador de columnas
                        linea += 1
                        columna = 1
                    columna += 1
                    
                else:
                    self.errores.append(TokenError(self.ERROR_LEXICO, caracter, linea, columna_actual))
                    columna += 1

            elif estado == 1:
                if caracter.isalnum():
                    lexema += caracter
                    
                else:
                    if lexema in self.keywords:
                        self.tokens.append(Token(self.PALABRA_RESERVADA, lexema, linea, columna_actual))
                    else:
                        # Esto sería error
                        self.errores.append(TokenError(self.ERROR_LEXICO, lexema, linea, columna_actual))
                    
                    lexema = ""
                    estado = 0
                
                    # si el caracter no es un espacio en blanco se guarda el caracter para poder analizarlo
                    if not caracter.isspace():
                        lexema += caracter
   
                    continue

            elif estado == 2:
                if caracter == '>':
                    lexema += caracter
                    self.tokens.append(Token(self.FLECHA, lexema, linea, columna_actual))
                    lexema = ""
                    estado = 0
                       
                else:
                    lexema += caracter
                    self.errores.append(TokenError(self.ERROR_LEXICO, lexema, linea, columna_actual))
                    lexema = ""
                    estado = 0
                    if not caracter.isspace():
                        columna -= 1
                        
            elif estado == 3:
                lexema += caracter
                if caracter == "'":
                    self.tokens.append(Token(self.STRING, lexema, linea, columna_actual))
                    lexema = ""
                    estado = 0
                elif caracter == '\n':
                    self.errores.append(TokenError(self.ERROR_LEXICO, lexema, linea, columna_actual))
                    lexema = ""
                    estado = 0
                    linea += 1
                    columna = 1
                    
            elif estado == 5:
                if self.esPunto(caracter):
                    lexema += caracter
                    if lexema == '...':
                        self.tokens.append(Token(self.SEPARADOR, lexema, linea, columna_actual))
                        # Crea una nueva imagen
                        self.lista_imagenes.append(self.tokens)
                        
                        # Reinicia la lista de tokens
                        self.tokens = []
                        
                        self.haySeparador = True
                        lexema = ""
                        estado = 0 
                else:
                    lexema += caracter  
                    self.errores.append(TokenError(self.ERROR_LEXICO, lexema, linea, columna_actual))
                    lexema = ""
                    estado = 0

            if not caracter.isspace() or estado == 3:
                columna += 1
        
        # Si no hay separador se guarda la imagen en la lista de imágenes
        self.lista_imagenes.append(self.tokens)
        
    def imprimir_tokens_y_errores(self):
        print("Tokens válidos:")
        for token in self.tokens:
            print(token)
        print("\nErrores léxicos:")
        for error in self.errores:
            print(error)

class GrafoParser:
    def __init__(self) -> None:
        self.lexer = Lexer()

    def parsear_grafos(self, contenido):
        self.lexer.analizar(contenido)
        lista_imagenes = self.lexer.lista_imagenes

        imagenes_procesadas = []

        for tokens in lista_imagenes:
            nodos = self.extraer_nodos(tokens)
            conexiones = self.extraer_conexiones(tokens)
            imagenes_procesadas.append({
                "nodos": nodos,
                "conexiones": conexiones
            })

        return imagenes_procesadas

    def extraer_nodos(self, tokens):
        NODOS = []

        i = 0
        while i < len(tokens):
            if tokens[i].nombre == 'Palabra Reservada' and tokens[i].lexema == 'nodos':
                i += 3  # Saltar "nodos -> ["
                while i < len(tokens) and tokens[i].nombre != 'Símbolo':
                    if tokens[i].nombre == 'String' and tokens[i + 1].lexema == ':' and tokens[i + 2].nombre == 'String':
                        nombre_nodo = tokens[i].lexema.strip("'")
                        texto_nodo = tokens[i + 2].lexema.strip("'")
                        NODOS.append([nombre_nodo, texto_nodo])
                        i += 4  # Avanzar más allá del conjunto 'nombre_nodo': 'texto_nodo'
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
                while i < len(tokens) and tokens[i].nombre != 'Símbolo':
                    if tokens[i].nombre == 'Símbolo' and tokens[i].lexema == '{':
                        i += 1
                        if tokens[i].nombre == 'String' and tokens[i + 1].nombre == 'Flecha' and tokens[i + 2].nombre == 'String':
                            nombre_nodo1 = tokens[i].lexema.strip("'")
                            nombre_nodo2 = tokens[i + 2].lexema.strip("'")
                            CONEXIONES.append([nombre_nodo1, nombre_nodo2])
                            i += 4  # Avanzar más allá del conjunto 'nombre_nodo1' > 'nombre_nodo2'
                        elif tokens[i].lexema == ',':
                            i += 1  # Saltar la coma
                        else:
                            i += 1
                    else:
                        i += 1
            else:
                i += 1

        return CONEXIONES

# Ejemplo de uso
contenido_prueba = """
nombre -> 'titulo';
nodos -> [
'nombre_nodo1': 'texto_nodo1',
'nombre_nodo2': 'texto_nodo2',
'nombre_nodo3': 'texto_nodo3'
];
conexiones ->[
{'nombre_nodo1' > 'nombre_nodo2'},
{'nombre_nodo3' > 'nombre_nodo2'}
]

...

nodos -> [
'nombre_nodo4': 'texto_nodo4',
'nombre_nodo5': 'texto_nodo5',
'nombre5': 'tdae'
];
conexiones ->[
{'nombre_nodo4' > 'nombre_nodo5'}
]
"""

parser = GrafoParser()
imagenes_procesadas = parser.parsear_grafos(contenido_prueba)

for idx, imagen in enumerate(imagenes_procesadas):
    print(f"Imagen {idx + 1}:")
    print("Nodos:", imagen["nodos"])
    print("Conexiones:", imagen["conexiones"])

