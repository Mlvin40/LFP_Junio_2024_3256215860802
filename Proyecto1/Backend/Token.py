class Token:
    #constructor que almacena toda la informacion necesaria del token
    def __init__(self, nombre, lexema, linea, columna ):
        self.nombre = nombre
        self.lexema = lexema
        self.linea = linea
        self.columna = columna  