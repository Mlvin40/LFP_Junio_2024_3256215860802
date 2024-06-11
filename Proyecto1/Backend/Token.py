class Token:
    #constructor que almacena toda la informacion necesaria del token
    def __init__(self, nombre, lexema, linea, columna ):
        self.nombre = nombre
        self.lexema = lexema
        self.linea = linea
        self.columna = columna  
        
    def __str__(self):
        return f'TOKEN: {self.nombre}, LEXEMA: {self.lexema}, LINEA: {self.linea}, COLUMNA: {self.columna}'
    
# token = f'TOKEN: Símbolo, Lexema: {lexema}, Línea: {linea}, Columna: {columna}'

