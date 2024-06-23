import sys
import os
# Añade la ruta del directorio principal al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Backend.Token import Token
from Backend.TokenError import TokenError

class Lexer:
    def __init__(self):
        self.tokens = []
        self.token_errors = []
        
        # Definicion de los tipos de tokens
        self.keywords = ['Array', 'new', 'sort', 'asc', 'FALSE', 'TRUE', 'save']
        
        # Definicion de los tipos de operadores
        self.operators = ['=', '.']
        
        # Definicion de los tipos de simbolos
        self.simbolos = ['[',']', ',', '(', ')', ';']
        
        # Constantes para los tipos de tokens
        self.PALABRA_CLAVE = "PalabraReservada"
        self.IDENTIFICADOR = "Identificador"
        self.ERROR_LEXICO = "Error lexico"
        self.CADENA = "Cadena"
        self.NUMERO = "Numero"
        self.SIMBOLO = "Simbolo"
        self.OPERADOR = "Operador"
        self.COMENTARIO = "Comentario"
        
    
    # Metodo para verificar si el caracter siguiente es un operador o un simbolo
    def verificarSeguido(self, caracter, linea ,columnaActual):
        if caracter in self.operators:
            self.tokens.append(Token(self.OPERADOR, caracter, linea, columnaActual))
            
        if caracter in self.simbolos:
            self.tokens.append(Token(self.SIMBOLO, caracter, linea, columnaActual))
            
    
    def analizar(self, texto):
        linea = 1 
        columna = 1
        lexema = ""
        estado = 0

        for caracter in texto:
            # Variable que almacena la columna actual
            columnaActual = columna - len(lexema)
             
            # Estado inicial
            if estado == 0:
                if caracter == '/':
                    lexema += caracter
                    estado = 1
            
                elif caracter.isalpha():
                    lexema += caracter
                    estado = 2
                    
                elif caracter in self.operators:
                    lexema += caracter
                    self.tokens.append(Token(self.OPERADOR, lexema, linea, columnaActual))
                    lexema = ""
                    
                elif caracter == '"':
                    lexema += caracter
                    estado = 4
                
                elif caracter in self.simbolos:
                    lexema += caracter
                    self.tokens.append(Token(self.SIMBOLO, lexema, linea, columnaActual))
                    lexema = ""
                    
                elif caracter.isspace():
                    if caracter == '\n': #si el caracter es un salto de linea se aumenta el contador de lineas y se reinicia el contador de columnas
                        linea += 1
                        columna = 1
                    columna += 1
                    
                elif caracter.isdigit or caracter == '-':
                    lexema += caracter
                    estado = 9
                           
                else :
                    self.token_errors.append(TokenError(self.ERROR_LEXICO, caracter, linea, columnaActual))
                    columna += 1
            
            elif estado == 1:
                if caracter == '/':
                    lexema += caracter
                    estado = 6
                
                elif caracter == '*':
                    lexema += caracter
                    estado = 7
                    
                else:
                    self.token_errors.append(TokenError(self.ERROR_LEXICO, lexema, linea, columnaActual))
                    lexema = ""
                    estado = 0 
            
            # Estado en donde se analiza el comentario de una linea
            elif estado == 6:
                if not caracter == '\n':
                    lexema += caracter
                else:
                    # Esto es un comentario de linea que se debe ignorar
                    lexema = ""
                    estado = 0
                    linea += 1
                    columna = 1
            
            # Estado en donde se analiza el comentario de bloque
            elif estado == 7:
                if caracter == '*':
                    lexema += caracter
                    estado = 8
                else:
                    lexema += caracter

            elif estado == 8:
                if caracter == '/':
                    # Esto es un comentario de bloque que se debe ignorar 
                    lexema = ""
                    estado = 0
                         
                else:
                    lexema += caracter
                    self.token_errors.append(TokenError(self.ERROR_LEXICO, lexema, linea, columnaActual))
                    lexema = ""
                    estado = 0
                    
            ################################## Verificar si se guarda el ultimo lexema ##################################
            # Estado en donde se analiza las palabras claves
            elif estado == 2:
                if caracter.isalnum():
                    # Si el caracter es alfanumerico o guion bajo se agrega al lexema
                    lexema += caracter or caracter == '_'
                else:
                    if lexema in self.keywords:
                        self.tokens.append(Token(self.PALABRA_CLAVE, lexema, linea, columnaActual))
                    else:
                        self.tokens.append(Token(self.IDENTIFICADOR, lexema, linea, columnaActual))
                    
                    # Verificar si el caracter siguiente es un operador o un simbolo cuando van en texto seguido
                    self.verificarSeguido(caracter, linea, columnaActual)
                        
                    lexema = ""
                    estado = 0
                
            # Estado en donde se analiza las cadenas de texto
            
            elif estado == 4:
                if caracter == '"':
                    lexema += caracter
                    self.tokens.append(Token(self.CADENA, lexema, linea, columnaActual))
                    lexema = ""
                    estado = 0
                else:
                    lexema += caracter
            
            elif estado == 9:
                # Estado para números (enteros o decimales)
                if caracter.isdigit() or caracter == '.':
                    lexema += caracter
                elif caracter.isalpha() or caracter in self.operators or caracter in self.simbolos or caracter.isspace():
                    # Si se encuentra un carácter que no pertenece a un número, finaliza la formación del token de número
                    self.tokens.append(Token(self.NUMERO, lexema, linea, columnaActual))
                    
                    # Verificar si el caracter siguiente es un operador o un simbolo cuando van en texto seguido
                    self.verificarSeguido(caracter, linea, columnaActual)
                    lexema = ""
                    estado = 0
                else:
                    # Error léxico si el caracter no es válido en un número
                    lexema += caracter
                    self.token_errors.append(TokenError(self.ERROR_LEXICO, lexema, linea, columnaActual))
                    lexema = ""
                    estado = 0            
                    
            # Incrementar el contador de columnas
            columna += 1
            

Lexer = Lexer()
contenido = """
// Editor de código fuente

// Comentario de una línea 

#
#

/*
Comentario
multilínea 
*/

Array miArray = new Array [ -15, 80.12, 68, 55, 48, "Hola" ];
miArray.sort(asc=FALSE);

miArray.save("ruta/del/archivo/csv");
"""

Lexer.analizar(contenido)
for token in Lexer.tokens:
    print(token)
    
print("\nErrores léxicos:")

for error in Lexer.token_errors:
    print(error)
            
            
            
            
                
            
                    
                
                
                
                    
                
                    
        