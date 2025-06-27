#!/usr/bin/env python

import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

def get_data_from_db_simulation():
    """
    Simula la obtención de datos de una base de datos.
    Aquí, cada entrada 'x' es un vector [x1, x2, x3, x4].
    """
    np.random.seed(42) # Para reproducibilidad

    data_points = []
    num_samples = 20 # Número de muestras de datos

    for _ in range(num_samples):
        x1 = np.random.uniform(0, 10)
        x2 = np.random.uniform(5, 15)
        x3 = np.random.uniform(10, 20)
        x4 = np.random.uniform(15, 25)
        y = (x1 * 0.5) + (x2 * 0.3) + (x3 * 0.2) - (x4 * 0.1) + np.random.normal(0, 1)
        data_points.append(([x1, x2, x3, x4], y))

    return data_points

def create_plot(frame):
    """
    Crea y muestra los gráficos en subplots en la ventana de Tkinter.
    Grafica 'y' contra cada 'xi' individualmente.
    """
    data = get_data_from_db_simulation()

    # Separa los vectores de x y los valores de y
    x_vectors = [d[0] for d in data]
    y_values = [d[1] for d in data]

    # Convertir a numpy arrays para facilitar el acceso a las columnas
    x_array = np.array(x_vectors)
    y_array = np.array(y_values)

    # Crea una figura de Matplotlib con 2x2 subplots
    fig, axes = Figure(figsize=(10, 8), dpi=100).subplots(nrows=2, ncols=2)
    fig.suptitle('Relación de la Imagen (y) con cada Componente del Dominio (xi)', fontsize=16)

    # Aplanar el array de axes para iterar fácilmente
    axes = axes.flatten()

    # Itera sobre cada dimensión de x (x1, x2, x3, x4)
    for i in range(4):
        axes[i].scatter(x_array[:, i], y_array, alpha=0.7, color='teal')
        axes[i].set_title(f'y vs x{i+1}')
        axes[i].set_xlabel(f'x{i+1}')
        axes[i].set_ylabel('y')
        axes[i].grid(True)

    # Ajusta el layout para evitar solapamientos
    fig.tight_layout(rect=[0, 0.03, 1, 0.95])

    # Embed la figura de Matplotlib en Tkinter
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    canvas.draw()

window = tk.Tk()

window.title("Supply Chain Optimization App")
window.geometry("800x600")

menu = tk.Menu(window)
item = tk.Menu(menu, tearoff=0)

item.add_command(label="Open", command=lambda: print("Open clicked"))
item.add_command(label="Quit", command=lambda: window.quit())
menu.add_cascade(label="App", menu=item)
window.config(menu=menu)

def on_button_click():
    print("Button clicked!")

button = tk.Button(window, text="Accept", command=on_button_click)
button.pack(pady=10)

progress_var = tk.DoubleVar()
progress_bar = ttk.Progressbar(window, orient="horizontal", length=300, mode="determinate", variable=progress_var, maximum=100)
progress_bar.pack(pady=20)

progress_var.set(0)

def update_progress():
    current_value = progress_var.get()
    if current_value < 100:
        progress_var.set(current_value + 10)
        window.after(1000, update_progress)
    else:
        print("Progress complete!")

start_button = tk.Button(window, text="Start Hill Climbing", command=update_progress)
start_button.pack(pady=10)

# Marco principal para el contenido
main_frame = tk.Frame(window)
main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Crea el gráfico dentro del marco principal
create_plot(main_frame)

window.mainloop()
