import sys
import os
# Añade la ruta del directorio principal al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Backend.Lexer import Lexer
from Backend.Token import Token

class Parser:
    def __init__(self, tokens) -> None:
        self.tokens = tokens
        self.tokens.append(Token('$', 'EOF', -1, -1))
        
    def error(self, message):
        print(f"Error sintáctico: {message} en la línea {self.tokens[0].linea} , columna {self.tokens[0].columna}")

    # Método para recuperar el modo pánico en caso de error
    def recuperar_modo_panico(self, nombre_tk_sincronizacion):
        while self.tokens[0].lexema != "$":
            if self.tokens[0].lexema == nombre_tk_sincronizacion:
                self.tokens.pop(0)
                break
            self.tokens.pop(0)
            
    def parse(self):
        self.inicio()
        
    # <inicio> ::= <instrucciones>
    def inicio(self):
        self.instrucciones()

    # <instrucciones> ::= <instruccion> <instrucciones>
    #                   | epsilon
    def instrucciones(self):
        if self.tokens[0].lexema == "EOF":
            return
        self.instruccion()
        self.instrucciones()

    # <instruccion> ::= <declaracion>
    #                 | <instruccionID>
    def instruccion(self):
        if self.tokens[0].lexema == "Array":
            self.declaracion()
        elif self.tokens[0].nombre == "Identificador":
            self.instruccionID()
        else:
            self.error("Se esperaba una declaración o una instrucción de ID")
            
    # <declaracion> ::= tk_palabraArray tk_id tk_igual tk_new tk_palabraArray tk_corcheteApertura <listaElementos> tk_corcheteCierre tk_puntoComa
    def declaracion(self):
        if self.tokens[0].lexema == "Array":
            self.tokens.pop(0)
            if self.tokens[0].nombre == "Identificador":
                id = self.tokens.pop(0)
                if self.tokens[0].lexema == "=":
                    self.tokens.pop(0)
                    if self.tokens[0].lexema == "new":
                        self.tokens.pop(0)
                        if self.tokens[0].lexema == "Array":
                            self.tokens.pop(0)
                            if self.tokens[0].lexema == "[":
                                self.tokens.pop(0)
                                elementos = self.listaElementos()
                                if self.tokens[0].lexema == "]":
                                    self.tokens.pop(0)
                                    if self.tokens[0].lexema == ";":
                                        self.tokens.pop(0)
                                        #Aquí se debe manejar la instruccion
                                        print(f"Declaración de Array: ID = {id.lexema}, Elementos = {[e.lexema for e in elementos]}")
                                    else:
                                        self.error("Se esperaba ';'")
                                else:
                                    self.error("Se esperaba ']'")
                            else:
                                self.error("Se esperaba '['")
                        else:
                            self.error("Se esperaba la palabra 'Array'")
                    else:
                        self.error("Se esperaba la palabra 'new'")
                else:
                    self.error("Se esperaba '='")
            else:
                self.error("Se esperaba un Identificador")
        else:
            self.error("Se esperaba la palabra 'Array'")

    # <listaElementos> ::= <elemento> tk_coma <listaElementos>
    #                    | <elemento>
    #                    | epsilon
    def listaElementos(self):
        item = self.elemento()
        if item is None:
            return []
        lista = [item]
        mas_elementos = self.mas_elementos()
        lista.extend(mas_elementos)
        return lista
    
    # <masElementos> ::= tk_coma <elemento> <masElementos>
    #                  | epsilon
    def mas_elementos(self):
        if self.tokens[0].lexema == ",":
            self.tokens.pop(0)
            item = self.elemento()
            if item is None:
                return []
            lista = [item]
            lista.extend(self.mas_elementos())
            return lista
        else:
            return []

    # <elemento> ::= tk_numero
    #              | tk_string
    def elemento(self):
        if self.tokens[0].nombre in ["Numero", "Cadena"]:
            return self.tokens.pop(0)
        else:
            return None

    # <instruccionID> ::= tk_id tk_punto <accionArreglo>
    def instruccionID(self):
        if self.tokens[0].nombre == "Identificador":
            id = self.tokens.pop(0)
            if self.tokens[0].lexema == ".":
                self.tokens.pop(0)
                self.accionArreglo(id)
            else:
                self.error("Se esperaba '.'")
                self.recuperar_modo_panico(";")
        else:
            self.error("Se esperaba un Identificador")

    # <accionArreglo> ::= <ordenamiento>
    #                   | <guardar>
    def accionArreglo(self, id_token):
        if self.tokens[0].lexema == "sort":
            self.ordenamiento(id_token)
        elif self.tokens[0].lexema == "save":
            self.guardar(id_token)
        else:
            self.error("Se esperaba una acción de arreglo ('sort' o 'save')")

    # <ordenamiento> ::= tk_sort tk_parentesisApertura tk_asc tk_igual tk_true tk_parentesisCierre tk_puntoComa
    #                  | tk_sort tk_parentesisApertura tk_asc tk_igual tk_false tk_parentesisCierre tk_puntoComa
    def ordenamiento(self, id_token):
        if self.tokens[0].lexema == "sort":
            self.tokens.pop(0)
            if self.tokens[0].lexema == "(":
                self.tokens.pop(0)
                if self.tokens[0].lexema == "asc":
                    self.tokens.pop(0)
                    if self.tokens[0].lexema == "=":
                        self.tokens.pop(0)
                        if self.tokens[0].lexema in ["TRUE", "FALSE"]:
                            asc_token = self.tokens.pop(0)
                            if self.tokens[0].lexema == ")":
                                self.tokens.pop(0)
                                if self.tokens[0].lexema == ";":
                                    self.tokens.pop(0)
                                    print(f"Ordenar Array: ID = {id_token.lexema}, Ascendente = {asc_token.lexema}")
                                else:
                                    self.error("Se esperaba ';'")
                            else:
                                self.error("Se esperaba ')'")
                        else:
                            self.error("Se esperaba 'TRUE' o 'FALSE'")
                    else:
                        self.error("Se esperaba '='")
                else:
                    self.error("Se esperaba 'asc'")
            else:
                self.error("Se esperaba '('")
        else:
            self.error("Se esperaba 'sort'")
            self.recuperar_modo_panico(";")

    # <guardar> ::= tk_save tk_parentesisApertura tk_string tk_parentesisCierre tk_puntoComa
    def guardar(self, id_token):
        if self.tokens[0].lexema == "save":
            self.tokens.pop(0)
            if self.tokens[0].lexema == "(":
                self.tokens.pop(0)
                if self.tokens[0].nombre == "Cadena":
                    path_token = self.tokens.pop(0)
                    if self.tokens[0].lexema == ")":
                        self.tokens.pop(0)
                        if self.tokens[0].lexema == ";":
                            self.tokens.pop(0)
                            # Handle save instruction
                            print(f"Guardar Array: ID = {id_token.lexema}, Ruta = {path_token.lexema}")
                        else:
                            self.error("Se esperaba ';'")
                    else:
                        self.error("Se esperaba ')'")
                else:
                    self.error("Se esperaba un string")
            else:
                self.error("Se esperaba '('")
        else:
            self.error("Se esperaba 'save'")
            #self.recuperar_modo_panico(";")
    # Fin de la clase Parser

        
Lexer = Lexer()

contenido = """
Array Prueba = new Array [ 15, 80, 68, 55, 48.13, -12.25 ];
miArray.sort(asc=FALSE);
miArray.save("ruta/del/archivo/csv");
"""

Lexer.analizar(contenido)

parser = Parser(Lexer.tokens)
parser.parse()

