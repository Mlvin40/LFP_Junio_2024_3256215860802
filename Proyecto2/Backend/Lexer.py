from Backend.Token import Token
from Backend.TokenError import TokenError

class Lexer:
    def __init__(self):
        self.tokens = []
        self.token_errors = []
        
        # Definicion de los tipos de tokens
        self.PALABRA_CLAVE = "Palabra clave"
        self.IDENTIFICADOR = "Identificador"
        self.keywords = ['Array', 'new', 'sort', 'asc', 'FALSE', 'TRUE', 'save']
        
        # Definicion de los tipos de operadores
        self.OPERADOR = "Operador"
        self.operators = ['=', '.']
        
        # Definicion de los tipos de simbolos
        self.SIMBOLO = "Simbolo"
        self.simbolos = ['[',']', ',', '(', ')', ';']
    
    def analizar(self, texto):
        linea = 1 
        columna = 1
        lexema = ""
        estado = 0
        
        for caracter in texto:
            columnaActual = columna - len(lexema)
            
            if estado == 0:
                if caracter == '/':
                    lexema += caracter
                    estado = 1
            
                elif caracter.isalpha():
                    lexema += caracter
                    estado = 2
                    
                elif caracter in self.operators:
                    lexema += caracter
                    estado = 3
                    
                elif caracter == '"':
                    lexema += caracter
                    estado = 4
                
                elif caracter in self.simbolos:
                    lexema += caracter
                    estado = 5
                    self.tokens.append(Token(self.SIMBOLO, lexema, linea, columnaActual))
            
                    
        