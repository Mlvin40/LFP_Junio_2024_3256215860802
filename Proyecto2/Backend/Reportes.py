class Reporte:
    def __init__(self) -> None:
        pass
        
    #Metodo que genera el reporte en formato HTML 
    def obtenerReporteTokens(self, tokens):
        contenido = """
        <html>
        <head>
            <title>Reporte Tokens</title>
            <style>
                table {
                    border-collapse: collapse;
                    width: 100%;
                }
                th, td {
                    padding: 6px;
                    text-align: left;
                    border: 1px solid #ddd;
                }
            </style>
        </head>
        <body>
            <h2>Reporte de Tokens</h2>
            <table>
                <thead>
                    <tr>
                        <th>Token</th>
                        <th>Lexema</th>
                        <th>Línea</th>
                        <th>Columna</th>
                    </tr>
                </thead>
                <tbody>
        """
        for token in tokens:
            contenido += f"""
                <tr>
                    <td>{token.nombre}</td>
                    <td>{token.lexema}</td>
                    <td>{token.linea}</td>
                    <td>{token.columna}</td>
                </tr>
            """
        contenido += """
                </tbody>
            </table>
        </body>
        </html>
        """
        return contenido
        
        
    def obtenerReporteErrores(self, lexicos, sintacticos):
        contenido = """
        <html>
        <head>
            <title>Reporte Errores</title>
            <style>
                table {
                    border-collapse: collapse;
                    width: 100%;
                }
                th, td {
                    padding: 6px;
                    text-align: left;
                    border: 1px solid #ddd;
                }
            </style>
        </head>
        <body>
            <h2>Reporte de Errores</h2>
            <h3>Errores Léxicos</h3>
            <table>
                <thead>
                    <tr>
                        <th>Error</th>
                        <th>Lexema</th>
                        <th>Línea</th>
                        <th>Columna</th>
                    </tr>
                </thead>
                <tbody>
        """
        for token in lexicos:
            contenido += f"""
                <tr>
                    <td>{token.error}</td>
                    <td>{token.lexema}</td>
                    <td>{token.linea}</td>
                    <td>{token.columna}</td>
                </tr>
            """

        contenido += """
                </tbody>
            </table>
            <h3>Errores Sintácticos</h3>
            <ul>
        """
        for error in sintacticos:
            contenido += f"<li>{error}</li>\n"

        contenido += """
            </ul>
        </body>
        </html>
        """
        return contenido