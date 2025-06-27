import sys, os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import db.config as dbconfig
import db.database as db

# Configuración de la base de datos
config = dbconfig.load_config('db/database.ini', 'supply_chain')
conn = db.get_connection(config)

query = """
    SELECT step, obj
    FROM experimento_hill_climbing
    WHERE estrategia = 'most_probable_scenario'
    ORDER BY step
"""
df = pd.read_sql(query, conn)
conn.close()

steps = df['step'].tolist()
valores_objetivo = df['obj'].tolist()

# Crear figura para animación
fig, ax = plt.subplots(figsize=(10, 5))
line, = ax.plot([], [], 'o-', color='green')
text = ax.text(0.5, 0.9, '', transform=ax.transAxes, ha='center')

ax.set_xlim(min(steps), max(steps))
ax.set_ylim(min(valores_objetivo) * 0.9995, max(valores_objetivo) * 1.0005)
ax.set_xlabel("Step")
ax.set_ylabel("Valor Objetivo")
ax.set_title("Evolución de Hill Climbing: most_probable_scenario")

def init():
    line.set_data([], [])
    text.set_text('')
    return line, text

def update(frame):
    xdata = steps[:frame + 1]
    ydata = valores_objetivo[:frame + 1]
    line.set_data(xdata, ydata)
    text.set_text(f'Step: {steps[frame]}, Obj: ${valores_objetivo[frame]:,.2f}')
    return line, text

anim = FuncAnimation(fig, update, frames=len(steps), init_func=init, blit=True, repeat=False)
plt.show()
plt.close()
