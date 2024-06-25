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
        self.errores_sintacticos = []
        self.cantidad_errores_sintacticos = 0
        
        self.lista_guardar = []
        self.lista_ordenar = []
        self.lista_elementos = []
        
    def error(self, message):
        print(f"Error sintáctico: {message} en la línea {self.tokens[0].linea} , columna {self.tokens[0].columna}")
        self.errores_sintacticos.append(f"Error sintáctico: {message} en la línea {self.tokens[0].linea} , columna {self.tokens[0].columna}")        
        self.cantidad_errores_sintacticos += 1
    
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
            self.recuperar_modo_panico(";")
            
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
                                        print("ID: ", id.lexema)
                                        print("Lista: ")
                                        for e in elementos:
                                            print(e.lexema)
                                        
                                        self.lista_elementos.append((id, elementos))    
                                                                                       
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
            self.recuperar_modo_panico(";")

    # <listaElementos> ::= <elemento> tk_coma(Simbolo) <listaElementos>
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
    
    # <masElementos> ::= tk_coma(Simbolo) <elemento> <masElementos>
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

    # <elemento> ::= tk_numero(Numero)
    #              | tk_string(Cadena)
    def elemento(self):
        if self.tokens[0].nombre in ["Numero", "Cadena"]:
            return self.tokens.pop(0)
        else:
            return None

    # <instruccionID> ::= tk_id(Identificador) tk_punto(Simbolo) <accionArreglo>
    def instruccionID(self):
        if self.tokens[0].nombre == "Identificador":
            id = self.tokens.pop(0)
            if self.tokens[0].lexema == ".":
                self.tokens.pop(0)
                self.accionArreglo(id)
                #print("la instruccionID es un ordenamiento para el arreglo", id.lexema, "con asc =", self.tokens[0].lexema)
            else:
                self.error("Se esperaba '.'")
                self.recuperar_modo_panico(";")
        else:
            self.error("Se esperaba un Identificador")
            self.recuperar_modo_panico(";")

    # <accionArreglo> ::= <ordenamiento>
    #                   | <guardar>
    def accionArreglo(self, id_token):
        if self.tokens[0].lexema == "sort":
            self.ordenamiento(id_token)
        elif self.tokens[0].lexema == "save":
            self.guardar(id_token)
        else:
            self.error("Se esperaba una acción de arreglo ('sort' o 'save')")
            self.recuperar_modo_panico(";")

    #<ordenamiento> ::= tk_sort(PalabraReservada) tk_parentesisApertura(Simbolo) tk_asc(PalabraReservada) tk_igual(Operador) tk_true(PalabraReservada) tk_parentesisCierre(Simbolo) tk_puntoComa(Simbolo)
    #                | tk_sort(PalabraReservada) tk_parentesisApertura(Simbolo) tk_asc(PalabraReservada) tk_igual(Operador) tk_false(PalabraReservada) tk_parentesisCierre(Simbolo) tk_puntoComa(Simbolo)
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
                                    # aqui se debe manejar la instruccion
                                    # ya tenemos el id del array y el valor de asc
                                    
                                    print(f"Ordenar : ID = {id_token.lexema}, Ascendente = {asc_token.lexema}")
                                    self.lista_ordenar.append((id_token, asc_token))
                                    
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
    
    # <guardar> ::= tk_save(PalabraReservada) tk_parentesisApertura(Simbolo) tk_string(Cadena) tk_parentesisCierre(Simbolo) tk_puntoComa(Simbolo)
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
                            
                            #Aquí se debe manejar la instruccion
                            #almacenar el id del array y la ruta del archivo
                               
                            print(f"Guardar : ID = {id_token.lexema}, Ruta = {path_token.lexema}")
                            self.lista_guardar.append((id_token, path_token))
                            
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
            self.recuperar_modo_panico(";")        
    # Fin de todo el parseo

Lexer = Lexer()

contenido2 = """
Array Prueb_a = new Array [ 15, 80, 68, 55, 48.13, -12.25 ];
Array Prueba_2 = new Array [ "hola", "mundo", "como", "estas" ];

miArray.save("ruta/del/archivo/csv");

miArray2.sort(asc=FALSE);
miArray2.save("ruta/del/archivo/csv");

Array Prueba3 = new Array [ 15, 80, 68, 55, 48.13, -12.25 ];
miArray3.sort(asc=TRUE);
miArray3.save("ruta/del/archivo/csv");

Array Prueba4 = new Array [ "hola", "mundo", "como", "estas" ];
miArray4.save("ruta/del/archivo/csv");
"""


contenido = """
Array myArray = new Array [ 15, 80, 68, 55, 48.13, -12.25 ];
miArray.sort(asc=TRUE);
miArray.save("ruta/del/archivo/csv");
"""

Lexer.analizar(contenido)

parser = Parser(Lexer.tokens)
parser.parse()


print("prueba de impresion de datos:")

print("\nlista de elementos:")
for lista in parser.lista_elementos:
    print("ID: ", lista[0].lexema)
    print("Elementos: ")
    for e in lista[1]:
        print(e.lexema)

print("\nlista de guardar:")
for lista in parser.lista_guardar:
    print("ID: ", lista[0].lexema)
    print("Ruta: ", lista[1].lexema)
    
print("\nlista de ordenar:")    
for lista in parser.lista_ordenar:
    print("ID: ", lista[0].lexema)
    print("Ascendente: ", lista[1].lexema)
