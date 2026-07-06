class GameController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.simulando = False
        self.velocidad_ms = 150
        
        # Vincular botones a funciones
        self.view.btn_play.config(command=self.toggle_simulacion)
        self.view.btn_reiniciar.config(command=self.reiniciar_modelo)
        
        self.actualizar_vista()

    def reiniciar_modelo(self):
        self.simulando = False
        try:
            nuevo_tamano = int(self.view.entry_tamano.get())
            nueva_prob = float(self.view.entry_prob.get())
            self.model.filas = nuevo_tamano
            self.model.columnas = nuevo_tamano
            self.model.prob_inicial = nueva_prob
        except ValueError:
            pass
            
        self.view.filas = self.model.filas
        self.view.columnas = self.model.columnas
        
        self.model.inicializar_matriz()
        self.actualizar_vista()

    def toggle_simulacion(self):
        self.simulando = not self.simulando
        if self.simulando:
            self._loop_simulacion()

    def _loop_simulacion(self):
        if self.simulando:
            self.model.siguiente_generacion()
            self.actualizar_vista()
            self.view.root.after(self.velocidad_ms, self._loop_simulacion)

    def actualizar_vista(self):
        self.view.dibujar_tablero(self.model.matriz, self.model.filas, self.model.columnas)
        self.view.actualizar_estadisticas(self.model.generacion, self.model.vivas, self.model.muertas)