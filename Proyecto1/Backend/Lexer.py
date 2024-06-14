import sys
import os

# Añadir el directorio raíz del proyecto al sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Backend.Token import Token
from Backend.Error import TokenError
from Backend.Reportes import Reporte

# Clase para analizar el código fuente y generar tokens
#######################


class Lexer:
    def __init__(self) -> None:
        self.entrada = ""
        self.keywords = {'nombre', 'nodos', 'conexiones'}
        self.tokens = []  # Lista para almacenar tokens válidos
        self.errores = []  # Lista para almacenar errores léxicos
        
        self.ERROR_LEXICO ="Identificador Desconocido"
        self.SIMBOLO = "Símbolo"
        self.PALABRA_RESERVADA = "Palabra Reservada"
        self.FLECHA = "Flecha"
        self.STRING = "String"
        self.SEPARADOR = "Separador"
        
        
    def isCaracterValido(self, caracter):
        return caracter in [';', '[', ']', ':', ',', '{', '}', '>']
    
    def esPunto(self, caracter):
        return caracter == '.'
    
    def analizar(self, entrada):
        #guarda la entrada de texto en la variable entrada para poder analizarla
        self.entrada = entrada
        
        linea = 1
        columna = 1
        lexema = ""
        estado = 0
        
        for caracter in self.entrada:
            #mantiene la columna en la que se encuentra el lexema actual
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
                    if caracter == '\n': #si el caracter es un salto de linea se aumenta el contador de lineas y se reinicia el contador de columnas
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
                        #Esto seria error
                        self.errores.append(TokenError(self.ERROR_LEXICO, lexema, linea, columna_actual))
                    
                    lexema = ""
                    estado = 0
                
                    #si el caracter no es un espacio en blanco se guarda el caracter para poder analizarlo
                    if not caracter.isspace():
                        lexema+= caracter
   
                    continue

            elif estado == 2:
                if caracter == '>':
                    lexema += caracter
                    self.tokens.append(Token(self.FLECHA, lexema, linea, columna_actual))
                    lexema = ""
                    estado = 0
                       
                else:
                    lexema+= caracter
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
                        lexema = ""
                        estado = 0 
                else :
                    lexema += caracter  
                    self.errores.append(TokenError(self.ERROR_LEXICO, lexema, linea, columna_actual))
                    lexema = ""
                    estado = 0

            if not caracter.isspace() or estado == 3:
                columna += 1
                
    def imprimir_tokens_y_errores(self):
        print("Tokens válidos:")
        for token in self.tokens:
            print(token)
        print("\nErrores léxicos:")
        for error in self.errores:
            print(error)
            
# Ejemplo de uso
contenido_prueba = """
nombre -> 'titulo';
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

lexer = Lexer()
lexer.analizar(contenido_prueba)
lexer.imprimir_tokens_y_errores()

