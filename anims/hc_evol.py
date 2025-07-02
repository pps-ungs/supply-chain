import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import pandas as pd
import sys, os
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import db.config as dbconfig
import db.database as db

config = dbconfig.load_config('db/database.ini', 'supply_chain')
conn = db.get_connection(config)

# Mejor experimento con mejor x inicial
query = """
    SELECT id, x_optimo, obj, step
    FROM experimento_hill_climbing
    WHERE experimento = '100_it_steps_based_on_915'
      AND estrategia = 'most_probable_scenario'
    ORDER BY id
"""

df = pd.read_sql(query, conn)
conn.close()

def x_label(x_optimo):
    x = json.loads(x_optimo)
    if isinstance(x[0], list):
        x = x[0]

    if len(x) > 4:
        return "[" + ", ".join(f"{v:.0f}" for v in x[:3]) + ", ...]"
    else:
        return "[" + ", ".join(f"{v:.0f}" for v in x) + "]"

df["X_label"] = df["x_optimo"].apply(x_label)

# Ejes
steps = df["step"].values
objs = df["obj"].values
labels = df["X_label"].values

fig, ax = plt.subplots(figsize=(10, 3))
sc = ax.scatter([], [], c=[], cmap='winter', vmin=objs.min(), vmax=objs.max())

line, = ax.plot([], [], color='#0d124b', alpha=0.6)  # Línea para unir los puntos

ax.set_xlim(steps.min() - 1, steps.max() + 1)

ymin = objs.min()
ymax = objs.max()
yrange = ymax - ymin

margen = 0.20 * yrange
ax.set_ylim(ymin - margen, ymax + margen)

ax.set_xlabel("Step")
ax.set_ylabel("Valor objetivo")

title = ax.set_title("Evolución del valor objetivo según step")
texts = []

# Encuentra el índice y valores del máximo
idx_max = objs.argmax()
x_max = steps[idx_max]
y_max = objs[idx_max]

# Línea punteada para el valor máximo
ax.axhline(y=y_max, color='#5666f8', linestyle='--', linewidth=1, alpha=0.7)

highlight = None  # Para el punto resaltado

def update(frame):
    global highlight
    for txt in texts:
        txt.remove()
    texts.clear()

    current = df.iloc[:frame+1]
    sc.set_offsets(np.c_[current["step"], current["obj"]])
    sc.set_array(current["obj"])
    line.set_data(current["step"], current["obj"])

    valor = current['obj'].iloc[-1]
    ganancia_str = f"${valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    title.set_text(f"Ganancia: {ganancia_str}")

    offset = yrange * 0.07
    for i, row in current.iterrows():
        posicion = 'bottom' if i % 2 == 0 else 'top'
        y = row["obj"] + (1 if posicion == 'bottom' else -1) * offset
        txt = ax.text(row["step"], y, row["X_label"], fontsize=10, ha='left', va=posicion)
        texts.append(txt)

    # Resalta el punto máximo solo si ya fue alcanzado en la animación
    if frame >= idx_max:
        if highlight:
            highlight.remove()
        highlight = ax.scatter(x_max, y_max, s=120, color='green', edgecolor='black', zorder=5)
        return sc, line, title, highlight, *texts
    else:
        if highlight:
            highlight.remove()
            highlight = None
        return sc, line, title, *texts

ani = animation.FuncAnimation(fig, update, frames=len(df), interval=700, blit=False)
ani.save("anims/gifs/evolucion_hill_climbing.gif", writer="pillow", fps=3)

plt.show()
plt.close(fig)
