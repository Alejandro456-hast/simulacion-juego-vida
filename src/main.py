import tkinter as tk
from model import GameModel
from view import GameView
from controller import GameController

def main():
    # Parámetros por defecto
    filas_iniciales = 30
    cols_iniciales = 40
    prob_inicial = 0.3

    # Instanciar el framework MVC
    root = tk.Tk()
    
    model = GameModel(filas_iniciales, cols_iniciales, prob_inicial)
    view = GameView(root, filas_iniciales, cols_iniciales)
    controller = GameController(model, view)
    
    root.mainloop()

if __name__ == "__main__":
    main()