import random
import csv
from datetime import datetime

class ModeloEpidemia:
    def __init__(self, filas, columnas, prob_contagio, dias_recuperacion, prob_fallecimiento, prob_vuelo):
        self.filas = filas
        self.columnas = columnas
        
        # Parámetros base
        self.prob_contagio_base = prob_contagio
        self.prob_vuelo_base = prob_vuelo
        self.dias_recuperacion = dias_recuperacion
        self.prob_fallecimiento = prob_fallecimiento
        
        # Parámetros dinámicos
        self.prob_contagio = prob_contagio
        self.prob_vuelo = prob_vuelo 
        self.cuarentena_activa = False
        
        self.matriz = [[0 for _ in range(columnas)] for _ in range(filas)]
        self.dias_infectado = {} 
        self.dia_actual = 0
        
        self.stats = {"sanas": 0, "infectadas": 0, "recuperadas": 0, "fallecidas": 0}
        self.historial = {"sanas": [], "infectadas": [], "recuperadas": [], "fallecidas": []}
        
        self.generar_mundo()

    def generar_mundo(self):
        for i in range(self.filas):
            for j in range(self.columnas):
                self.matriz[i][j] = 1 if random.random() < 0.58 else 0

        for _ in range(5): 
            nueva = [[0]*self.columnas for _ in range(self.filas)]
            for i in range(self.filas):
                for j in range(self.columnas):
                    vecinos = self._contar_estado(i, j, 1)
                    if self.matriz[i][j] == 1 and vecinos >= 3: nueva[i][j] = 1
                    elif self.matriz[i][j] == 0 and vecinos >= 5: nueva[i][j] = 1
                    else: nueva[i][j] = 0
            self.matriz = nueva

        self.dias_infectado.clear()
        self.historial = {"sanas": [], "infectadas": [], "recuperadas": [], "fallecidas": []}
        self.cuarentena_activa = False
        self.prob_contagio = self.prob_contagio_base
        self.prob_vuelo = self.prob_vuelo_base

        tierra = [(i, j) for i in range(self.filas) for j in range(self.columnas) if self.matriz[i][j] == 1]
        if tierra:
            pacientes_cero = random.sample(tierra, min(2, len(tierra)))
            for i, j in pacientes_cero:
                self.matriz[i][j] = 2
                self.dias_infectado[(i, j)] = 0
                
        self.dia_actual = 0
        self.actualizar_estadisticas()

    def toggle_cuarentena(self):
        self.cuarentena_activa = not self.cuarentena_activa
        if self.cuarentena_activa:
            # CUARENTENA ESTRICTA: Reduce el contagio al 2% de su valor base (Aplanamiento real)
            self.prob_contagio = self.prob_contagio_base * 0.02 
            self.prob_vuelo = 0.0 # Cierre total de fronteras aéreas
        else:
            self.prob_contagio = self.prob_contagio_base
            self.prob_vuelo = self.prob_vuelo_base

    def _contar_estado(self, fila, col, estado):
        count = 0
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if i == 0 and j == 0: continue
                r, c = (fila + i) % self.filas, (col + j) % self.columnas
                if self.matriz[r][c] == estado: count += 1
        return count

    def siguiente_dia(self):
        nueva_matriz = [fila[:] for fila in self.matriz]
        nuevos_dias = self.dias_infectado.copy()
        
        for i in range(self.filas):
            for j in range(self.columnas):
                estado = self.matriz[i][j]
                
                if estado == 1: 
                    vecinos_inf = self._contar_estado(i, j, 2)
                    if vecinos_inf > 0:
                        prob = 1 - ((1 - self.prob_contagio) ** vecinos_inf)
                        if random.random() < prob:
                            nueva_matriz[i][j] = 2
                            nuevos_dias[(i, j)] = 0
                            
                elif estado == 2: 
                    if random.random() < self.prob_vuelo:
                        ri, rj = random.randint(0, self.filas-1), random.randint(0, self.columnas-1)
                        if nueva_matriz[ri][rj] == 1: 
                            nueva_matriz[ri][rj] = 2
                            nuevos_dias[(ri, rj)] = 0

                    nuevos_dias[(i, j)] += 1
                    if nuevos_dias[(i, j)] >= self.dias_recuperacion:
                        if random.random() < self.prob_fallecimiento:
                            nueva_matriz[i][j] = 4 
                        else:
                            nueva_matriz[i][j] = 3 
                        del nuevos_dias[(i, j)]
                        
        self.matriz = nueva_matriz
        self.dias_infectado = nuevos_dias
        self.dia_actual += 1
        self.actualizar_estadisticas()

    def actualizar_estadisticas(self):
        self.stats = {"sanas": 0, "infectadas": 0, "recuperadas": 0, "fallecidas": 0}
        for fila in self.matriz:
            for celda in fila:
                if celda == 1: self.stats["sanas"] += 1
                elif celda == 2: self.stats["infectadas"] += 1
                elif celda == 3: self.stats["recuperadas"] += 1
                elif celda == 4: self.stats["fallecidas"] += 1
                
        self.historial["sanas"].append(self.stats["sanas"])
        self.historial["infectadas"].append(self.stats["infectadas"])
        self.historial["recuperadas"].append(self.stats["recuperadas"])
        self.historial["fallecidas"].append(self.stats["fallecidas"])

    def exportar_datos_csv(self):
        if not self.historial["sanas"]: return None
        fecha = datetime.now().strftime('%Y%m%d_%H%M%S')
        nombre_archivo = f"reporte_epidemia_{fecha}.csv"
        
        with open(nombre_archivo, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["Dia", "Sanas", "Infectadas", "Recuperadas", "Fallecidas"])
            for i in range(len(self.historial["sanas"])):
                writer.writerow([
                    i, 
                    self.historial["sanas"][i], 
                    self.historial["infectadas"][i], 
                    self.historial["recuperadas"][i], 
                    self.historial["fallecidas"][i]
                ])
        return nombre_archivo