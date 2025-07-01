import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import os
import sys
import numpy as np
import pandas as pd
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import db.config as dbconfig
import db.database as db

EXPERIMENTO_A_ANIMAR = 'equal_factories_1000_iterations_less_rho_200_prod_2'

config = dbconfig.load_config('db/database.ini', 'supply_chain')
conn = db.get_connection(config)

query = f"""
    SELECT historial_x, historial_z, iteraciones_realizadas
    FROM experimento_aco
    WHERE experimento = '{EXPERIMENTO_A_ANIMAR}'
"""
df_experiment_row = pd.read_sql(query, conn)
conn.close()

if df_experiment_row.empty:
    print(f"No se encontraron datos para el experimento: '{EXPERIMENTO_A_ANIMAR}'")
    exit()
elif len(df_experiment_row) > 1:
    print(f"Advertencia: Se encontraron múltiples entradas para el experimento '{EXPERIMENTO_A_ANIMAR}'. Se usará la primera.")
    experiment_data = df_experiment_row.iloc[0]
else:
    experiment_data = df_experiment_row.iloc[0]

try:
    historial_x_full = json.loads(experiment_data['historial_x'])
    historial_x_full = [sol if isinstance(sol, list) else [sol] for sol in historial_x_full]
except (json.JSONDecodeError, TypeError):
    print(f"Error: No se pudo parsear historial_x del experimento '{EXPERIMENTO_A_ANIMAR}'.")
    historial_x_full = []

try:
    historial_z_full = json.loads(experiment_data['historial_z'])
    historial_z_full = [float(z) for z in historial_z_full]
except (json.JSONDecodeError, ValueError, TypeError):
    print(f"Error: No se pudo parsear historial_z del experimento '{EXPERIMENTO_A_ANIMAR}'.")
    historial_z_full = []

filtered_iterations = []
filtered_obj_sequence = []
filtered_x_full = []

last_z_value = None
for i in range(min(len(historial_z_full), len(historial_x_full))):
    current_z = historial_z_full[i]
    current_x = historial_x_full[i]

    if last_z_value is None or (current_z not in filtered_obj_sequence and current_x not in filtered_x_full):
        filtered_obj_sequence.append(current_z)
        filtered_x_full.append(current_x)
        filtered_iterations.append(i + 1)
    last_z_value = current_z

num_iterations_filtered = len(filtered_obj_sequence)

if num_iterations_filtered == 0:
    print("No hay iteraciones únicas para animar. Saliendo.")
    exit()

iterations_sequence = np.array(filtered_iterations)
obj_sequence = np.array(filtered_obj_sequence)

def x_label_formatter(x_solution):
    if not isinstance(x_solution, list):
        x_solution = [x_solution]
    
    if len(x_solution) > 4:
        return "[" + ", ".join(f"{v:.0f}" for v in x_solution[:3]) + ", ...]"
    else:
        return "[" + ", ".join(f"{v:.0f}" for v in x_solution) + "]"

x_labels_sequence = [x_label_formatter(x_sol) for x_sol in filtered_x_full]

# --- Configuración inicial del gráfico ---
fig, ax = plt.subplots(figsize=(10, 5))
ax.set_facecolor('#d1d2db')
fig.patch.set_facecolor('#d1d2db')

sc = ax.scatter([], [], c=[], cmap='viridis', vmin=obj_sequence.min(), vmax=obj_sequence.max())
line, = ax.plot([], [], color='#0d124b', alpha=0.6, linewidth=2)

ax.set_xlim(0, iterations_sequence.max() + 1 if iterations_sequence.size > 0 else 1)

ymin = obj_sequence.min()
ymax = obj_sequence.max()
yrange = ymax - ymin
margen = 0.30 * yrange
ax.set_ylim(ymin - margen, ymax + margen)

ax.set_xlabel("Número de Iteración")
ax.set_ylabel("Valor Objetivo")
title = ax.set_title(f"Evolución del valor objetivo por iteración.")
texts = []

best_z_overall = obj_sequence.max()
idx_best_z = np.argmax(obj_sequence)
iter_best_z = iterations_sequence[idx_best_z]

print("AAAAAAAAAA", best_z_overall, idx_best_z, iter_best_z, x_labels_sequence[idx_best_z])

ax.axhline(y=best_z_overall, color='#5666f8', linestyle='--', linewidth=1, alpha=0.7, zorder=4)

highlight_best_point = None

def update(frame_idx):
    global highlight_best_point
    for txt in texts:
        txt.remove()
    texts.clear()

    current_iterations = iterations_sequence[:frame_idx+1]
    current_objs = obj_sequence[:frame_idx+1]
    current_x_labels = x_labels_sequence[:frame_idx+1]
    
    sc.set_offsets(np.c_[current_iterations, current_objs])
    sc.set_array(current_objs)
    
    line.set_data(current_iterations, current_objs)

    current_z_value = current_objs[-1]
    z_str = f"Ganancia: ${current_z_value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    title.set_text(z_str)

    offset = yrange * 0.07
    indices_to_label = []
    
    if len(current_iterations) > 0:
        indices_to_label.append(len(current_iterations) - 1)
    
    step_display = max(1, num_iterations_filtered // 10)
    for i in range(0, len(current_iterations) - 1, step_display):
        if i not in indices_to_label:
            indices_to_label.append(i)
            
    indices_to_label.sort()

    for idx_in_current_data in indices_to_label:
        iter_val_original = current_iterations[idx_in_current_data]
        if idx_in_current_data % 2 != 0:
            obj_val = current_objs[idx_in_current_data]
            x_lbl = current_x_labels[idx_in_current_data]
            y_text = obj_val + 1 * offset
            
            txt = ax.text(iter_val_original, y_text, x_lbl, 
                        fontsize=10, 
                        ha='left',
                        va="top") 
            texts.append(txt)

    if frame_idx >= idx_best_z:
        if highlight_best_point:
            highlight_best_point.remove()
        highlight_best_point = ax.scatter(iter_best_z, best_z_overall, s=120, color='green', edgecolor='black', zorder=5)
    else:
        if highlight_best_point:
            highlight_best_point.remove()
            highlight_best_point = None

        return sc, line, title, highlight_best_point, *texts

ani = animation.FuncAnimation(fig, update, frames=num_iterations_filtered, interval=400, blit=False)

gif_path = f"anims/gifs/evolucion_aco.gif"
ani.save(gif_path, writer="pillow", fps=3)

plt.show()
plt.close(fig)