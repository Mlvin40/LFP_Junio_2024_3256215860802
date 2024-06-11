class Lexer:
    def __init__(self, entrada) -> None:
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
        inicio_lexema_columna = 1  # Guardar la columna de inicio de cada lexema

        for caracter in self.entrada:
            if estado == 0:
                if caracter.isalpha():
                    lexema += caracter
                    estado = 1
                    inicio_lexema_columna = columna
                elif caracter == "-":
                    lexema += caracter
                    estado = 2
                    inicio_lexema_columna = columna
                elif caracter == "'":
                    lexema += caracter
                    estado = 3
                    inicio_lexema_columna = columna
                elif self.isCaracterValido(caracter):
                    lexema += caracter
                    token = f'TOKEN: Símbolo, Lexema: {lexema}, Línea: {linea}, Columna: {columna}'
                    self.tokens.append(token)
                    lexema = ""
                elif caracter.isspace():
                    if caracter == '\n':
                        linea += 1
                        columna = 0
                    columna += 1
                else:
                    self.error_lexico("Carácter inesperado", caracter, linea, columna)
                    columna += 1

            elif estado == 1:
                if caracter.isalnum() or caracter == '_':
                    lexema += caracter
                else:
                    if lexema in self.keywords:
                        token = f'TOKEN: Palabra Reservada, Lexema: {lexema}, Línea: {linea}, Columna: {inicio_lexema_columna}'
                    else:
                        #esto seria error
                        token = f'ERROR: Identificador Desconocido, Lexema: {lexema}, Línea: {linea}, Columna: {inicio_lexema_columna}'
                    self.tokens.append(token)
                    lexema = ""
                    estado = 0
                    continue

            elif estado == 2:
                if caracter == '>':
                    lexema += caracter
                    token = f'TOKEN: FLECHA, Lexema: {lexema}, Línea: {linea}, Columna: {inicio_lexema_columna}'
                    self.tokens.append(token)
                    lexema = ""
                    estado = 0
                else:
                    self.error_lexico("Carácter inesperado", lexema, linea, inicio_lexema_columna)
                    lexema = ""
                    estado = 0
                    if not caracter.isspace():
                        columna -= 1

            elif estado == 3:
                lexema += caracter
                if caracter == "'":
                    token = f'TOKEN: String, Lexema: {lexema}, Línea: {linea}, Columna: {inicio_lexema_columna}'
                    self.tokens.append(token)
                    lexema = ""
                    estado = 0
                elif caracter == '\n':
                    self.errores.append
                    self.error_lexico("Fin de línea inesperado en cadena", lexema, linea, inicio_lexema_columna)
                    lexema = ""
                    estado = 0

            if not caracter.isspace() or estado == 3:
                columna += 1

    def error_lexico(self, mensaje, lexema, linea, columna):
        error = f'ERROR LEXICO: {mensaje}, Lexema: {lexema}, Línea: {linea}, Columna: {columna}'
        self.tokens.append(error)
    
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
{'nombre_   nodo1' > 'nombre_nodo2'},
{'nombre_nodo3' > 'nombre_nodo2'}
]
"""

lexer = Lexer(contenido_prueba)
lexer.analizar()
lexer.imprimir_tokens_y_errores()