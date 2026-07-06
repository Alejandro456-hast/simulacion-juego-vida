import tkinter as tk
from model import ModeloEpidemia
from view import VistaEpidemia
from controller import ControladorEpidemia

def main():
    filas = 45
    columnas = 80
    
    root = tk.Tk()
    root.resizable(False, False) 
    
    modelo = ModeloEpidemia(filas, columnas, prob_contagio=0.20, dias_recuperacion=12, prob_fallecimiento=0.06, prob_vuelo=0.005)
    vista = VistaEpidemia(root, filas, columnas)
    controlador = ControladorEpidemia(modelo, vista)
    
    root.mainloop()

if __name__ == "__main__":
    main()