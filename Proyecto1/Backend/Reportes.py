class Reporte:
    def __init__(self, entrada, tipo) -> None:
        self.entrada = entrada
        self.tipo = tipo
        
    #Metodo que genera el reporte en formato HTML 
    def obtenerReporte(self):
        contenido = ""
        for token in self.entrada:
            #contenido += f"{str(token)}<br/>\n"
            
            contenido += f"<p>{str(token)}</p>\n"
        
        reporte = f"""<html>
                        <head>
                            <title>Reporte {self.tipo}</title>
                        </head>
                        <body>
{contenido}
                        </body>
                      </html>"""
        return reporte
        