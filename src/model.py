import random

class GameModel:
    def __init__(self, filas, columnas, prob_inicial):
        self.filas = filas
        self.columnas = columnas
        self.prob_inicial = prob_inicial
        self.matriz = []
        self.generacion = 0
        self.vivas = 0
        self.muertas = 0
        self.inicializar_matriz()

    def inicializar_matriz(self):
        # 0 = Muerta. >0 = Viva (el número representa la "edad" de la célula)
        self.matriz = [[0 for _ in range(self.columnas)] for _ in range(self.filas)]
        self.generacion = 0
        for i in range(self.filas):
            for j in range(self.columnas):
                if random.random() < self.prob_inicial:
                    self.matriz[i][j] = 1 
        self._actualizar_conteos()

    def _contar_vecinos_vivos(self, fila, col):
        vecinos = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                r = (fila + i) % self.filas
                c = (col + j) % self.columnas
                if self.matriz[r][c] > 0:
                    vecinos += 1
        return vecinos

    def siguiente_generacion(self):
        nueva_matriz = [[0 for _ in range(self.columnas)] for _ in range(self.filas)]
        
        for i in range(self.filas):
            for j in range(self.columnas):
                vecinos = self._contar_vecinos_vivos(i, j)
                edad_actual = self.matriz[i][j]
                
                if edad_actual > 0 and (vecinos == 2 or vecinos == 3):
                    nueva_matriz[i][j] = edad_actual + 1  # Sobrevive y envejece
                elif edad_actual == 0 and vecinos == 3:
                    nueva_matriz[i][j] = 1  # Nace
                else:
                    nueva_matriz[i][j] = 0  # Muere
                    
        self.matriz = nueva_matriz
        self.generacion += 1
        self._actualizar_conteos()

    def _actualizar_conteos(self):
        self.vivas = sum(1 for fila in self.matriz for celda in fila if celda > 0)
        self.muertas = (self.filas * self.columnas) - self.vivas