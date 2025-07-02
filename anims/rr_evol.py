import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import db.config as dbconfig
import db.database as db

config = dbconfig.load_config('db/database.ini', 'supply_chain')
conn = db.get_connection(config)

query = """
    SELECT x_optimo, obj
    FROM experimento_random_restart
    WHERE experimento = '10_loops_10_restarts'
    ORDER BY obj
"""
df = pd.read_sql(query, conn)
conn.close()

if df.empty:
    print("No hay datos para mostrar.")
    exit()

df["id"] = df.index + 1

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
ids = df["id"].values
objs = df["obj"].values
labels = df["X_label"].values

fig, ax = plt.subplots(figsize=(8, 3))

sc = ax.scatter([], [], c=[], cmap='viridis', vmin=objs.min(), vmax=objs.max())
line, = ax.plot([], [], color='#0d124b', alpha=0.6)

ax.set_xlim(ids.min() - 1, ids.max() + 1)

ymin = objs.min()
ymax = objs.max()
yrange = ymax - ymin
margen = 0.20 * yrange
ax.set_ylim(ymin - margen, ymax + margen)

ax.set_xlabel("Mejora (id)")
ax.set_ylabel("Valor objetivo")
title = ax.set_title("Evolución del valor objetivo por mejora (Random Restart)")
texts = []

# Encuentra el índice y valores del máximo
idx_max = objs.argmax()
x_max = ids[idx_max]
y_max = objs[idx_max]

# Línea horizontal para el valor máximo
hline, = ax.plot([ids.min(), ids.max()], [y_max, y_max], color='#5666f8', linestyle='--', linewidth=1, alpha=0.7, zorder=4)
hline.set_visible(False)
highlight = None

def update(frame):
    global highlight
    for txt in texts:
        txt.remove()
    texts.clear()

    current = df.iloc[:frame+1]
    sc.set_offsets(np.c_[current["id"], current["obj"]])
    sc.set_array(current["obj"])
    line.set_data(current["id"], current["obj"])

    valor = current['obj'].iloc[-1]
    ganancia_str = f"${valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    title.set_text(f"Ganancia: {ganancia_str}")

    offset = yrange * 0.07
    for i, row in current.iterrows():
        posicion = 'bottom' if i % 2 == 0 else 'top'
        y = row["obj"] + (1 if posicion == 'bottom' else -1) * offset
        txt = ax.text(row["id"], y, row["X_label"], fontsize=10, ha='left', va=posicion)
        texts.append(txt)

    if frame >= idx_max:
        if highlight:
            highlight.remove()
        highlight = ax.scatter(x_max, y_max, s=120, color='green', edgecolor='black', zorder=5)
        hline.set_visible(True)
    else:
        if highlight:
            highlight.remove()
            highlight = None
        hline.set_visible(False)

    return sc, line, title, hline, highlight, *texts

ani = animation.FuncAnimation(fig, update, frames=len(df), interval=700, blit=False)
ani.save("anims/gifs/evolucion_random_restart.gif", writer="pillow", fps=3)

plt.show()
plt.close(fig)