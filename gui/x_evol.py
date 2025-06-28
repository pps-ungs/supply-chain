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

fig, ax = plt.subplots(figsize=(10, 6))
sc = ax.scatter([], [], c=[], cmap='viridis', vmin=objs.min(), vmax=objs.max())

line, = ax.plot([], [], color='gray', alpha=0.6)  # Línea para unir los puntos

ax.set_xlim(steps.min() - 1, steps.max() + 1)
ax.set_ylim(objs.min() - 500, objs.max() + 500)
ax.set_xlabel("Step")
ax.set_ylabel("Valor objetivo")

title = ax.set_title("Evolución del valor objetivo según step")
texts = []

def update(frame):
    for txt in texts:
        txt.remove()
    texts.clear()

    current = df.iloc[:frame+1]
    sc.set_offsets(np.c_[current["step"], current["obj"]])
    sc.set_array(current["obj"])
    line.set_data(current["step"], current["obj"])  # Actualiza la línea

    valor = current['obj'].iloc[-1]
    ganancia_str = f"${valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    title.set_text(f"Ganancia: {ganancia_str}")

    # Etiquetas para cada punto
    for i, row in current.iterrows():
        txt = ax.text(row["step"], row["obj"], row["X_label"], fontsize=8, ha='left', va='top')
        texts.append(txt)
    return sc, line, title, *texts

ani = animation.FuncAnimation(fig, update, frames=len(df), interval=300, blit=False)
plt.show()
plt.close(fig)
