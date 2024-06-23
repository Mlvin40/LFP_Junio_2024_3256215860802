from Backend.Lexer import Lexer

if __name__ == '__main__':
 
    Lexer = Lexer()
    contenido = """
    Array miArray = new Array [ -15, 80.12, 68, 55, 48, "Hola" ];
    miArray.sort(asc=FALSE);

    miArray.save("ruta/del/archivo/csv");
    """

    Lexer.analizar(contenido)
    for token in Lexer.tokens:
        print(token)
        
    print("\nErrores léxicos:")

    for error in Lexer.token_errors:
        print(error)
                