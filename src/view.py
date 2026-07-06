import tkinter as tk

class GameView:
    def __init__(self, root, filas, columnas):
        self.root = root
        self.root.title("Simulador Complejo: Juego de la Vida")
        self.root.configure(bg="#2c3e50")
        
        self.tamano_celda = 15
        self.filas = filas
        self.columnas = columnas
        
        self._crear_interfaz()

    def _crear_interfaz(self):
        # Panel de controles oscuro moderno
        self.frame_controles = tk.Frame(self.root, padx=15, pady=15, bg="#34495e")
        self.frame_controles.pack(side=tk.LEFT, fill=tk.Y)
        
        tk.Label(self.frame_controles, text="CONFIGURACIÓN", font=("Segoe UI", 12, "bold"), fg="white", bg="#34495e").pack(pady=10)
        
        tk.Label(self.frame_controles, text="Dimensión (N):", fg="white", bg="#34495e").pack()
        self.entry_tamano = tk.Entry(self.frame_controles, width=10, bg="#ecf0f1")
        self.entry_tamano.insert(0, str(self.filas))
        self.entry_tamano.pack(pady=5)
        
        tk.Label(self.frame_controles, text="Prob. Inicial (0.1 - 1.0):", fg="white", bg="#34495e").pack()
        self.entry_prob = tk.Entry(self.frame_controles, width=10, bg="#ecf0f1")
        self.entry_prob.insert(0, "0.3")
        self.entry_prob.pack(pady=5)
        
        self.btn_reiniciar = tk.Button(self.frame_controles, text="↻ Aplicar Cambios", bg="#f39c12", fg="white", font=("Segoe UI", 10, "bold"), relief="flat")
        self.btn_reiniciar.pack(pady=15, fill=tk.X)
        
        self.btn_play = tk.Button(self.frame_controles, text="▶ Iniciar / Pausar", bg="#27ae60", fg="white", font=("Segoe UI", 10, "bold"), relief="flat")
        self.btn_play.pack(pady=5, fill=tk.X)
        
        # Resultados
        tk.Label(self.frame_controles, text="ESTADÍSTICAS", font=("Segoe UI", 12, "bold"), fg="white", bg="#34495e").pack(pady=20)
        self.lbl_gen = tk.Label(self.frame_controles, text="Generación: 0", fg="#ecf0f1", bg="#34495e", font=("Segoe UI", 10))
        self.lbl_gen.pack(anchor=tk.W)
        self.lbl_vivas = tk.Label(self.frame_controles, text="Vivas: 0", fg="#2ecc71", bg="#34495e", font=("Segoe UI", 10, "bold"))
        self.lbl_vivas.pack(anchor=tk.W)
        self.lbl_muertas = tk.Label(self.frame_controles, text="Muertas: 0", fg="#e74c3c", bg="#34495e", font=("Segoe UI", 10))
        self.lbl_muertas.pack(anchor=tk.W)

        # Tablero
        self.canvas = tk.Canvas(self.root, width=self.columnas*self.tamano_celda, height=self.filas*self.tamano_celda, bg="#1a1a1a", highlightthickness=0)
        self.canvas.pack(side=tk.RIGHT, padx=20, pady=20)

    def dibujar_tablero(self, matriz, filas, columnas):
        self.canvas.delete("all")
        self.canvas.config(width=columnas*self.tamano_celda, height=filas*self.tamano_celda)
        
        for i in range(filas):
            for j in range(columnas):
                edad = matriz[i][j]
                if edad == 0:
                    continue  # No dibujamos células muertas (queda el fondo oscuro)
                elif edad == 1:
                    color = "#00ffcc"  # Neón brillante para recién nacidas
                elif edad == 2:
                    color = "#00cc99"
                elif edad == 3:
                    color = "#009966"
                else:
                    color = "#006633"  # Verde oscuro para las más viejas
                    
                x1, y1 = j * self.tamano_celda, i * self.tamano_celda
                self.canvas.create_rectangle(x1, y1, x1+self.tamano_celda-1, y1+self.tamano_celda-1, fill=color, outline="")

    def actualizar_estadisticas(self, gen, vivas, muertas):
        self.lbl_gen.config(text=f"Generación: {gen}")
        self.lbl_vivas.config(text=f"Vivas: {vivas}")
        self.lbl_muertas.config(text=f"Muertas: {muertas}")