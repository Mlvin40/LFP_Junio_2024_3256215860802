class Lexer:
    def __init__(self, entrada):
        self.entrada = entrada
        self.keywords = {'nombre', 'nodos', 'conexiones'}
        self.tokens = []  # Lista para almacenar tokens válidos
        self.errores = []  # Lista para almacenar errores léxicos

    def isCaracterValido(self, caracter):
        return caracter in [';', '[', ']', ':', ',', '{', '}', '>']


    def analizar(self):
        linea = 1
        columna = 1
        lexema = ""
        estado = 0

        for caracter in self.entrada:
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
                    estado = 4
                elif caracter.isspace():
                    if caracter == '\n':
                        linea += 1
                        columna = 1
                    else:
                        columna += 1
                else:
                    print(f'ERROR LÉXICO: {caracter} ({linea}, {columna})')
                    
            elif estado == 1:
                if caracter.isalnum() or caracter == '_':
                    lexema += caracter
                else:
                    print(f'IDENTIFICADOR: {lexema} ({linea}, {columna - len(lexema)})')
                    lexema = ""
                    estado = 0
                    continue
            elif estado == 2:
                if caracter == '>':
                    lexema += caracter
                    print(f'OPERADOR: {lexema} ({linea}, {columna - len(lexema)})')
                    lexema = ""
                    estado = 0
                else:
                    print(f'ERROR LÉXICO: {caracter} ({linea}, {columna})')
                    estado = 0
            elif estado == 3:
                if caracter == "'":
                    lexema += caracter
                    print(f'STRING: {lexema} ({linea}, {columna - len(lexema)})')
                    lexema = ""
                    estado = 0
                elif caracter == '\n':
                    print(f'ERROR LÉXICO: Fin de línea inesperado ({linea}, {columna})')
                    estado = 0
                else:
                    lexema += caracter
            elif estado == 4:
                print(f'SÍMBOLO: {lexema} ({linea}, {columna - len(lexema)})')
                lexema = ""
                estado = 0
                continue
            if not caracter.isspace():
                columna += 1
                
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
lexer = Lexer(contenido_prueba)
lexer.analizar()