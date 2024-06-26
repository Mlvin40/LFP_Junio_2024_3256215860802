class Ordenamiento:
    def __init__(self) -> None:
        pass
    
    # Ordenamiento por burbuja ascendente según valor numérico (lexema si es numérico)
    def burbujaAscendente(self, lista):
        n = len(lista)
        for i in range(n - 1):
            for j in range(0, n - i - 1):
                if self.comparar(lista[j].lexema, lista[j + 1].lexema) > 0:
                    lista[j], lista[j + 1] = lista[j + 1], lista[j]
        return lista

    # Ordenamiento por burbuja descendente según valor numérico (lexema si es numérico)
    def burbujaDescendente(self, lista):
        n = len(lista)
        for i in range(n - 1):
            for j in range(0, n - i - 1):
                if self.comparar(lista[j].lexema, lista[j + 1].lexema) < 0:
                    lista[j], lista[j + 1] = lista[j + 1], lista[j]
        return lista

    def comparar(self, a, b):
        try:
            # Intentar convertir a float
            float_a = float(a)
            float_b = float(b)
            # Si se pueden convertir a float, comparar numéricamente
            if float_a < float_b:
                return -1
            elif float_a > float_b:
                return 1
            else:
                return 0
        except ValueError:
            # Si no se pueden convertir a float, comparar alfabéticamente
            if a < b:
                return -1
            elif a > b:
                return 1
            else:
                return 0