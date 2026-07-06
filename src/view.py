import tkinter as tk
from tkinter import messagebox

class VistaEpidemia:
    def __init__(self, root, filas, columnas):
        self.root = root
        self.root.title("Simulador Epidemiológico Nivel PRO")
        self.root.configure(bg="#0f172a") 
        self.tamano_celda = 10  
        self.filas = filas
        self.columnas = columnas
        
        self.construir_interfaz()

    def construir_interfaz(self):
        fuente_titulo = ("Segoe UI", 14, "bold")
        fuente_texto = ("Segoe UI", 10, "bold")
        fuente_desc = ("Segoe UI", 8, "italic")
        bg_panel = "#1e293b"
        
        # Panel Izquierdo: Controles
        panel_izq = tk.Frame(self.root, bg=bg_panel, padx=20, pady=20)
        panel_izq.pack(side=tk.LEFT, fill=tk.Y)
        
        tk.Label(panel_izq, text="SALA DE CONTROL", font=fuente_titulo, fg="#38bdf8", bg=bg_panel).pack(pady=(0, 10))
        
        self._crear_input(panel_izq, "Prob. Contagio:", "0.20", "Ej: 0.8 = Virus muy contagioso", "ent_contagio", fuente_texto, fuente_desc, bg_panel)
        self._crear_input(panel_izq, "Días Recuperación:", "12", "Ej: 5 = Se cura rápido", "ent_recuperacion", fuente_texto, fuente_desc, bg_panel)
        self._crear_input(panel_izq, "Prob. Fallecimiento:", "0.06", "Ej: 0.5 = 50% letalidad", "ent_muerte", fuente_texto, fuente_desc, bg_panel)
        self._crear_input(panel_izq, "Prob. Vuelos Globales:", "0.005", "Ej: 0.1 = Muchos vuelos infectados", "ent_vuelo", fuente_texto, fuente_desc, bg_panel)
        
        self.btn_aplicar = tk.Button(panel_izq, text="Generar Nuevo Mundo", bg="#475569", fg="white", font=("Segoe UI", 10), relief="flat")
        self.btn_aplicar.pack(fill=tk.X, pady=(15, 5))
        
        self.btn_play = tk.Button(panel_izq, text="▶ INICIAR BROTE", bg="#e11d48", fg="white", font=("Segoe UI", 12, "bold"), relief="flat", pady=5)
        self.btn_play.pack(fill=tk.X)

        # NUEVO: Botones de Intervención y Datos
        self.btn_cuarentena = tk.Button(panel_izq, text="🛡️ DECLARAR CUARENTENA", bg="#f59e0b", fg="white", font=("Segoe UI", 10, "bold"), relief="flat", state="disabled")
        self.btn_cuarentena.pack(fill=tk.X, pady=(10, 5))

        self.btn_exportar = tk.Button(panel_izq, text="📊 Exportar Datos CSV", bg="#10b981", fg="white", font=("Segoe UI", 10), relief="flat")
        self.btn_exportar.pack(fill=tk.X)

        # Dashboard de Estadísticas
        caja_stats = tk.Frame(panel_izq, bg="#0f172a", bd=0, pady=10, padx=15)
        caja_stats.pack(fill=tk.X, pady=15)
        
        self.lbl_dia = tk.Label(caja_stats, text="DÍA: 0", fg="#38bdf8", bg="#0f172a", font=("Segoe UI", 14, "bold"))
        self.lbl_dia.pack(anchor=tk.W, pady=(0,5))
        
        self.lbl_sanas = tk.Label(caja_stats, text="Sanas: 0", fg="#10b981", bg="#0f172a", font=fuente_texto)
        self.lbl_sanas.pack(anchor=tk.W)
        self.lbl_infectadas = tk.Label(caja_stats, text="Infectadas: 0", fg="#f43f5e", bg="#0f172a", font=("Segoe UI", 11, "bold"))
        self.lbl_infectadas.pack(anchor=tk.W)
        self.lbl_recuperadas = tk.Label(caja_stats, text="Recuperadas: 0", fg="#3b82f6", bg="#0f172a", font=fuente_texto)
        self.lbl_recuperadas.pack(anchor=tk.W)
        self.lbl_fallecidas = tk.Label(caja_stats, text="Fallecidas: 0", fg="#94a3b8", bg="#0f172a", font=fuente_texto)
        self.lbl_fallecidas.pack(anchor=tk.W)

        # Paneles derechos
        panel_der = tk.Frame(self.root, bg="#0f172a")
        panel_der.pack(side=tk.RIGHT, padx=20, pady=20)

        # NUEVO: Leyenda Visual
        leyenda = tk.Frame(panel_der, bg="#0f172a")
        leyenda.pack(fill=tk.X, pady=(0, 5))
        self._crear_item_leyenda(leyenda, "#14532d", "Sana")
        self._crear_item_leyenda(leyenda, "#ff0000", "Brote Reciente")
        self._crear_item_leyenda(leyenda, "#8b0000", "Infección Grave")
        self._crear_item_leyenda(leyenda, "#0284c7", "Recuperada (Inmune)")
        self._crear_item_leyenda(leyenda, "#334155", "Fallecida")

        self.canvas_mapa = tk.Canvas(panel_der, width=self.columnas*self.tamano_celda, height=self.filas*self.tamano_celda, bg="#020617", highlightthickness=0)
        self.canvas_mapa.pack(pady=(0, 10))

        self.h_grafica = 120
        self.w_grafica = self.columnas*self.tamano_celda
        self.canvas_grafica = tk.Canvas(panel_der, width=self.w_grafica, height=self.h_grafica, bg="#1e293b", highlightthickness=0)
        self.canvas_grafica.pack()

    def _crear_item_leyenda(self, parent, color, texto):
        frame = tk.Frame(parent, bg="#0f172a")
        frame.pack(side=tk.LEFT, padx=5)
        tk.Label(frame, text="■", fg=color, bg="#0f172a", font=("Arial", 12)).pack(side=tk.LEFT)
        tk.Label(frame, text=texto, fg="#cbd5e1", bg="#0f172a", font=("Segoe UI", 8)).pack(side=tk.LEFT)

    def _crear_input(self, parent, label_text, default_val, desc_text, attr_name, font_lbl, font_desc, bg_color):
        tk.Label(parent, text=label_text, fg="#f8fafc", bg=bg_color, font=font_lbl).pack(anchor=tk.W, pady=(8,0))
        entry = tk.Entry(parent, bg="#334155", fg="white", insertbackground="white", relief="flat")
        entry.insert(0, default_val)
        entry.pack(fill=tk.X, pady=2, ipady=3)
        tk.Label(parent, text=desc_text, fg="#94a3b8", bg=bg_color, font=font_desc).pack(anchor=tk.W)
        setattr(self, attr_name, entry)

    def actualizar_mapa(self, matriz, dias_infectado, dias_recup_max):
        self.canvas_mapa.delete("all")
        for i, fila in enumerate(matriz):
            for j, estado in enumerate(fila):
                if estado == 0: continue 
                if estado == 2:
                    dias = dias_infectado.get((i, j), 0)
                    intensidad = max(0, 255 - int((dias / dias_recup_max) * 150))
                    color = f"#{intensidad:02x}0000" 
                else:
                    colores = {1: "#14532d", 3: "#0284c7", 4: "#334155"}
                    color = colores[estado]
                
                x1, y1 = j * self.tamano_celda, i * self.tamano_celda
                self.canvas_mapa.create_rectangle(x1, y1, x1+self.tamano_celda, y1+self.tamano_celda, fill=color, outline="")

    def actualizar_estadisticas(self, dia, stats):
        self.lbl_dia.config(text=f"DÍA: {dia}")
        self.lbl_sanas.config(text=f"Sanas: {stats['sanas']}")
        self.lbl_infectadas.config(text=f"Infectadas: {stats['infectadas']}")
        self.lbl_recuperadas.config(text=f"Recuperadas: {stats['recuperadas']}")
        self.lbl_fallecidas.config(text=f"Fallecidas: {stats['fallecidas']}")

    def dibujar_grafica(self, historial):
        self.canvas_grafica.delete("all")
        dias = len(historial["sanas"])
        if dias < 2: return

        max_pob = max(max(historial["sanas"]), max(historial["infectadas"]), max(historial["recuperadas"]), max(historial["fallecidas"]))
        if max_pob == 0: max_pob = 1

        ancho_paso = self.w_grafica / (dias - 1)
        
        self._trazar_linea(historial["sanas"], max_pob, ancho_paso, "#10b981")     
        self._trazar_linea(historial["infectadas"], max_pob, ancho_paso, "#f43f5e") 
        self._trazar_linea(historial["recuperadas"], max_pob, ancho_paso, "#3b82f6")
        self._trazar_linea(historial["fallecidas"], max_pob, ancho_paso, "#94a3b8") 

    def _trazar_linea(self, datos, max_pob, ancho_paso, color):
        puntos = []
        for dia, valor in enumerate(datos):
            x = dia * ancho_paso
            y = self.h_grafica - (valor / max_pob * self.h_grafica)
            puntos.extend([x, y])
        if len(puntos) >= 4:
            self.canvas_grafica.create_line(puntos, fill=color, width=2)
            
    def mostrar_mensaje(self, titulo, mensaje):
        messagebox.showinfo(titulo, mensaje)