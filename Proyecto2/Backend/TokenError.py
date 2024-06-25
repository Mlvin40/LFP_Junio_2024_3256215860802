class TokenError:
    #constructor que almacena a los errores detectados
    def __init__(self, error, lexema, linea, columna ):
        self.error = error
        self.lexema = lexema
        self.linea = linea
        self.columna = columna  
        
    def __str__(self):
        return f'Error: {self.error}, LEXEMA: {self.lexema}, LINEA: {self.linea}, COLUMNA: {self.columna}'
    
