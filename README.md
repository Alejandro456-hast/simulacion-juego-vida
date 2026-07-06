# Simulación Epidemiológica Global mediante Autómatas Celulares

## 1. Introducción y Objetivo del Proyecto
El presente proyecto tiene como objetivo desarrollar una simulación de propagación epidémica utilizando la teoría de autómatas celulares bidimensionales. Alejándose de la cuadrícula clásica del Juego de la Vida de Conway, esta herramienta implementa un modelo **SIR modificado (Susceptible, Infectado, Recuperado, Fallecido)** sobre un mundo generado procedimentalmente, permitiendo analizar la evolución dinámica del contagio en el tiempo mediante reglas locales y eventos estocásticos.

## 2. Características Principales
* **Arquitectura MVC:** Código estructurado profesionalmente en Modelo, Vista y Controlador para máxima eficiencia y mantenibilidad.
* **Mapa de Calor Dinámico:** Visualización basada en continentes generados aleatoriamente, donde el color de las células infectadas se oscurece dependiendo de su carga viral (días de infección).
* **Gráfica Epidemiológica en Tiempo Real:** Trazado de líneas dinámicas que muestran la evolución poblacional (aplanamiento de la curva) día a día.
* **Intervención Estatal:** Botón interactivo de "Cuarentena" que permite modificar las variables de contagio y vuelos en tiempo real para observar el impacto de las políticas públicas.
* **Exportación de Datos:** Capacidad de exportar el censo diario a formato `.csv` para su posterior análisis y validación estadística (Pruebas de Medias, Varianza, Chi-Cuadrada).

## 3. Reglas de Transición (Modelo Epidemiológico)
Cada celda evalúa su estado actual y el de sus 8 vecinas (Vecindad de Moore) para decidir su próximo estado:
1. **Infección Local:** Una célula sana se infecta según una probabilidad acumulada basada en la cantidad de vecinos infectados a su alrededor.
2. **Movilidad Global (Vuelos):** Una célula infectada tiene una probabilidad de teletransportar el virus a cualquier otra coordenada sana del mapa, creando nuevos focos.
3. **Resolución Médica:** Tras un número determinado de días, la célula evalúa su probabilidad de letalidad; si sobrevive, pasa al estado recuperado (inmune).

## 4. Requisitos y Configuración del Entorno
Una de las mayores ventajas de este proyecto es su ligereza y nula dependencia de paquetes externos de terceros.

* **Intérprete:** Se requiere tener instalado **Python 3.x**.
* **Librerías:** El proyecto utiliza exclusivamente librerías nativas de Python (`tkinter`, `random`, `csv`, `datetime`). **No se requieren instalaciones mediante `pip`.**

## 5. Instrucciones de Ejecución
1. Clonar este repositorio o descargar los archivos.
2. Abrir una terminal y navegar hasta el directorio de los códigos fuente:
   ```bash
   cd src