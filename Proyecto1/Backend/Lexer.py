class Lexer:
    
    #entrada es el texto que obtiene al cargar un archivo
    def __init__(self, entrada) -> None:
        self.entrada = entrada

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
                else:
                    print(f'ERROR LÉXICO: {caracter} ({linea}, {columna})')
                    
                    
    def textoPrueba():
        return """
        nombre -> 'titulo';
        nodos -> [
            'nombre_nodo1': 'texto_nodo1',
            'nombre_nodo2': 'texto nodo2',
            'nombre_nodo3': 'texto_nodo3'
        ];
        conexiones ->[
            {'nombre_nodo1 > 'nombre nodo2'},
            {'nombre_nodo3 > 'nombre_nodo2'}
        ]
        """
              
    print(textoPrueba())