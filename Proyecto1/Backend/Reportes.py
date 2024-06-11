class Reporte:
    def __init__(self, entrada) -> None:
        self.entrada = entrada
        
    def obtenerReporte(self):
        
        cotenido = ""
        
        for lineas in self.entrada:
            cotenido += lineas + "<\n>"
        
        reporte= ("<html>" + "\n"
                + " <head>" + "\n" 
                + "     <title>Reporte Partida</title>" + "\n"
                + " </head>" + "\n"
                + "     <body>" + "\n"
                + cotenido
                + "     </body>" + "\n"
                + "</html>");
        return cotenido
        