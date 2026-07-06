class ControladorEpidemia:
    def __init__(self, modelo, vista):
        self.modelo = modelo
        self.vista = vista
        self.corriendo = False
        self.velocidad = 100 
        self.after_id = None 
        
        self.vista.btn_play.config(command=self.toggle_simulacion)
        self.vista.btn_aplicar.config(command=self.reiniciar)
        self.vista.btn_cuarentena.config(command=self.toggle_cuarentena)
        self.vista.btn_exportar.config(command=self.exportar_csv)
        
        self.sincronizar_vista()

    def reiniciar(self):
        self.corriendo = False
        if self.after_id is not None:
            self.vista.root.after_cancel(self.after_id)
            self.after_id = None

        self.vista.btn_play.config(text="▶ INICIAR BROTE", state="normal", bg="#e11d48")
        self.vista.btn_cuarentena.config(text="🛡️ DECLARAR CUARENTENA", bg="#f59e0b", state="disabled")
        
        try:
            self.modelo.prob_contagio_base = float(self.vista.ent_contagio.get())
            self.modelo.dias_recuperacion = int(self.vista.ent_recuperacion.get())
            self.modelo.prob_fallecimiento = float(self.vista.ent_muerte.get())
            self.modelo.prob_vuelo_base = float(self.vista.ent_vuelo.get())
        except ValueError:
            pass 

        self.modelo.generar_mundo()
        self.sincronizar_vista()

    def toggle_cuarentena(self):
        self.modelo.toggle_cuarentena()
        if self.modelo.cuarentena_activa:
            self.vista.btn_cuarentena.config(text="⚠️ LEVANTAR CUARENTENA", bg="#8b5cf6")
        else:
            self.vista.btn_cuarentena.config(text="🛡️ DECLARAR CUARENTENA", bg="#f59e0b")

    def exportar_csv(self):
        archivo = self.modelo.exportar_datos_csv()
        if archivo:
            self.vista.mostrar_mensaje("Exportación Exitosa", f"Datos guardados correctamente en:\n{archivo}")
        else:
            self.vista.mostrar_mensaje("Error", "No hay datos para exportar. Corre la simulación primero.")

    def toggle_simulacion(self):
        self.corriendo = not self.corriendo
        if self.corriendo:
            self.vista.btn_play.config(text="⏸ PAUSAR", bg="#ea580c")
            self.vista.btn_cuarentena.config(state="normal")
            self.bucle_principal()
        else:
            self.vista.btn_play.config(text="▶ REANUDAR", bg="#e11d48")

    def bucle_principal(self):
        if not self.corriendo: return

        if self.modelo.stats["infectadas"] == 0 and self.modelo.dia_actual > 0:
            self.corriendo = False
            self.vista.btn_play.config(text="PLAGA ERRADICADA", state="disabled", bg="#475569")
            self.vista.btn_cuarentena.config(state="disabled")
            return

        self.modelo.siguiente_dia()
        self.sincronizar_vista()
        self.after_id = self.vista.root.after(self.velocidad, self.bucle_principal)

    def sincronizar_vista(self):
        self.vista.actualizar_mapa(self.modelo.matriz, self.modelo.dias_infectado, self.modelo.dias_recuperacion)
        self.vista.actualizar_estadisticas(self.modelo.dia_actual, self.modelo.stats)
        self.vista.dibujar_grafica(self.modelo.historial)