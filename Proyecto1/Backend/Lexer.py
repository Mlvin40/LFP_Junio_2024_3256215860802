from Backend.Token import Token
from Backend.Error import TokenError
from Backend.Reportes import Reporte

# Clase para analizar el código fuente y generar tokens
#######################


class Lexer:
    def __init__(self, entrada) -> None:
        self.entrada = entrada
        self.keywords = {'nombre', 'nodos', 'conexiones'}
        self.tokens = []  # Lista para almacenar tokens válidos
        self.errores = []  # Lista para almacenar errores léxicos

    def isCaracterValido(self, caracter):
        return caracter in [';', '[', ']', ':', ',', '{', '}', '>']
    
    def esPunto(self, caracter):
        return caracter == '.'

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
                    self.tokens.append(Token("Símbolo", lexema, linea, columna - len(lexema)))
                    lexema = ""
                    
                elif caracter == '.':
                    lexema += caracter
                    estado = 5
                    
                elif caracter.isspace():
                    if caracter == '\n':
                        linea += 1
                        columna = 1
                    columna += 1
                else:
                    self.errores.append(TokenError("Carácter inesperado", caracter, linea, columna - len(lexema)))
                    columna += 1

            elif estado == 1:
                if caracter.isalnum():
                    lexema += caracter
                else:
                    if lexema in self.keywords:
                        self.tokens.append(Token("Palabra Reservada", lexema, linea, columna - len(lexema)))
                    else:
                        #Esto seria error
                        self.errores.append(TokenError("Identificador Desconocido", lexema, linea, columna - len(lexema)))
                    
                    lexema = ""
                    estado = 0
                
                    #si el caracter no es un espacio en blanco se guarda el caracter para poder analizarlo
                    if not caracter.isspace():
                        lexema+= caracter
   
                    continue

            elif estado == 2:
                if caracter == '>':
                    lexema += caracter
                    self.tokens.append(Token("FLECHA", lexema, linea, columna - len(lexema)))
                    lexema = ""
                    estado = 0
                       
                else:
                    lexema+= caracter
                    self.errores.append(TokenError("Carácter inesperado", lexema, linea, columna - len(lexema)))
                    lexema = ""
                    estado = 0
                    if not caracter.isspace():
                        columna -= 1
                        
            elif estado == 3:
                lexema += caracter
                if caracter == "'":
                    self.tokens.append(Token("String", lexema, linea, columna - len(lexema)))
                    lexema = ""
                    estado = 0
                elif caracter == '\n':
                    self.errores.append(TokenError("Fin de línea inesperado en cadena", lexema, linea, columna - len(lexema)))
                    lexema = ""
                    estado = 0
                    
            elif estado == 5:
                if caracter == '.':
                    lexema += caracter
                    if lexema == '...':
                        self.tokens.append(Token("Separador", lexema, linea, columna - len(lexema)))
                        lexema = ""
                        estado = 0 
                else :
                    lexema += caracter  
                    self.errores.append(TokenError("Carácter inesperado", lexema, linea, columna - len(lexema)))
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

.
..
... 
....

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


"""from tkinter import filedialog, Tk, Label, Button, Text, Canvas, ttk

def reporte_T():
    ruta_reporte = filedialog.asksaveasfilename(defaultextension=".html", filetypes=[("Archivos HTML", "*.html")])
    
    # Verificar si se ha seleccionado una ubicación y un nombre de archivo
    if ruta_reporte:
        try:
            # Crear el archivo con el nombre especificado en la ubicación seleccionada
            with open(ruta_reporte, 'w') as file:
                file.write(htmp)
                
                print("Reporte guardado en:", ruta_reporte)
        except Exception as e:
            print("Error al guardar el reporte:", e)


lexer = Lexer(contenido_prueba)
lexer.analizar()

lexer.imprimir_tokens_y_errores()
repor = Reporte(lexer.tokens, "Tokens")
htmp = repor.obtenerReporte()
reporte_T()
print(htmp)"""
