# SUPPAI — SUPPly chAIn Optimizer

**SUPPAI** es una aplicación de optimización de cadenas de distribución desarrollada en Python. Utiliza heurísticas de búsqueda local y metaheurísticas para maximizar la ganancia esperada en una red de distribución de tres niveles: **centros de fabricación → centros de distribución → puntos de venta**, bajo múltiples escenarios de demanda estocástica.

---

## Tabla de contenidos

- [Descripción del problema](#descripción-del-problema)
- [Arquitectura del sistema](#arquitectura-del-sistema)
- [Algoritmos implementados](#algoritmos-implementados)
- [Función objetivo](#función-objetivo)
- [Estructura del proyecto](#estructura-del-proyecto)
- [Requisitos](#requisitos)
- [Instalación y configuración](#instalación-y-configuración)
- [Uso](#uso)
  - [Interfaz gráfica (GUI)](#interfaz-gráfica-gui)
  - [Ejecución por línea de comandos](#ejecución-por-línea-de-comandos)
  - [Generación de datos de entrada](#generación-de-datos-de-entrada)
- [Base de datos](#base-de-datos)
- [Experimentos y animaciones](#experimentos-y-animaciones)
- [Autores y licencia](#autores-y-licencia)

---

## Descripción del problema

El sistema modela una **cadena de distribución básica** compuesta por tres tipos de nodos:

| Símbolo | Elemento                  | Descripción                                              |
|---------|---------------------------|----------------------------------------------------------|
| **F**   | Centros de fabricación    | Producen una cantidad `x_i` de producto                  |
| **S**   | Centros de distribución   | Reciben el producto de las fábricas y lo envían a ventas |
| **P**   | Puntos de venta           | Venden el producto al consumidor final                   |
| **E**   | Escenarios de demanda     | Conjunto de demandas posibles, generadas por Monte Carlo |

El objetivo es determinar la **cantidad óptima a producir en cada fábrica** (`X = {x_1, ..., x_kF}`) de modo de maximizar la ganancia esperada, considerando:

- El **margen de ganancia** por unidad vendida en cada punto de venta.
- La **penalidad por stock sobrante** al final del período.
- La **penalidad por demanda insatisfecha** en cada punto de venta.
- Los **costos de transporte** desde fábricas a centros de distribución, y desde estos a puntos de venta.

La distribución de los productos entre nodos sigue **curvas de distribución** predefinidas.

---

## Arquitectura del sistema

```
Fábricas (F)
    │  (curva cf: cuánto envía cada fábrica a cada centro de distribución)
    ▼
Centros de distribución (S)
    │  (curva cp: cuánto envía cada centro a cada punto de venta)
    ▼
Puntos de venta (P)
    │  (demanda estocástica por escenario)
    ▼
Stock sobrante (Y) / Demanda insatisfecha (Z)
```

Los **escenarios de demanda** (`E`) se generan mediante simulación de Monte Carlo usando distribuciones estadísticas (normal, uniforme, Poisson o binomial) y se almacenan en la base de datos.

---

## Algoritmos implementados

### 1. Hill Climbing (Escalador de colinas)

Búsqueda local que, partiendo de una solución inicial, explora una **vecindad** de soluciones vecinas en cada iteración y avanza hacia la de mayor valor objetivo. Se detiene cuando:

- La mejora entre iteraciones es menor que un umbral `epsilon` (solución satisfactoria).
- Se alcanza el número máximo de iteraciones.
- Se queda atascado en un óptimo local.

**Parámetros principales:**

| Parámetro            | Descripción                                                  |
|----------------------|--------------------------------------------------------------|
| `step`               | Tamaño del paso para explorar la vecindad                    |
| `epsilon`            | Tolerancia mínima de mejora para continuar                   |
| `max_iterations_allowed` | Número máximo de iteraciones                            |
| `initial_X`          | Solución inicial (vector de cantidades a producir)           |

---

### 2. Random Restart (Reinicio aleatorio)

Extiende Hill Climbing ejecutándolo **múltiples veces** con distintos puntos de partida aleatorios. Conserva la mejor solución encontrada a lo largo de todos los reinicios. Se detiene cuando:

- Se alcanza el número máximo de reinicios.
- Se supera el número máximo de ciclos sin mejora.

**Parámetros adicionales respecto a Hill Climbing:**

| Parámetro                    | Descripción                                              |
|------------------------------|----------------------------------------------------------|
| `max_restarts`               | Número máximo de reinicios                               |
| `max_loops_without_improvement` | Ciclos consecutivos sin mejora antes de detenerse   |

---

### 3. Ant Colony Optimization — ACO (Colonia de hormigas)

Metaheurística inspirada en el comportamiento de las hormigas reales. Cada **hormiga** construye una solución candidata eligiendo niveles de producción de forma probabilística, guiada por:

- **Rastros de feromonas** (τ): representan la "memoria colectiva" de buenas soluciones anteriores.
- **Información heurística** (η): favorece niveles de producción con mejor rendimiento esperado.

En cada iteración:
1. Cada hormiga construye una solución.
2. La mejor hormiga de la iteración deposita feromonas.
3. Las feromonas se evaporan según la tasa `ρ`.
4. Se actualizan los límites τ_min y τ_max (estrategia MMAS).

**Parámetros principales:**

| Parámetro          | Descripción                                                           |
|--------------------|-----------------------------------------------------------------------|
| `alpha` (α)        | Importancia del rastro de feromonas (0–1)                            |
| `beta` (β)         | Importancia de la información heurística (generalmente > 1)          |
| `rho` (ρ)          | Tasa de evaporación de feromonas (0–1)                               |
| `Q`                | Constante para el cálculo del depósito de feromonas                  |
| `tau_min` / `tau_max` | Límites mínimo y máximo del rastro de feromonas                  |
| `num_prod_levels`  | Número de niveles de producción discretos que puede elegir cada hormiga |
| `num_ants`         | Cantidad de hormigas en la colonia                                    |
| `max_iterations`   | Número máximo de iteraciones                                         |

---

## Función objetivo

La función objetivo a **maximizar** es:

```
Z = margen - pStk - pDIn - CTf2s - CTs2p
```

Donde:

| Término   | Descripción                                                                         |
|-----------|-------------------------------------------------------------------------------------|
| `margen`  | Ganancia bruta esperada por productos vendidos en los puntos de venta               |
| `pStk`    | Penalidad esperada por stock sobrante en los puntos de venta                        |
| `pDIn`    | Penalidad esperada por demanda insatisfecha en los puntos de venta                  |
| `CTf2s`   | Costo total de transporte de fábricas a centros de distribución                     |
| `CTs2p`   | Costo total de transporte de centros de distribución a puntos de venta              |

La expectativa se calcula sobre todos los escenarios de demanda `E`, ponderados por su probabilidad de ocurrencia `π_l` (equiprobable por defecto).

---

## Estructura del proyecto

```
supply-chain/
├── main.py                   # Punto de entrada CLI: ejecuta los tres algoritmos
├── setup.py                  # Creación, restauración y lectura de la base de datos
├── input_generator.py        # Generación de datos sintéticos de entrada
│
├── models/
│   ├── model.py              # Clase base abstracta (función objetivo, parámetros)
│   ├── hill_climbing.py      # Heurística Hill Climbing
│   ├── random_restart.py     # Heurística Random Restart
│   ├── ant_colony.py         # Metaheurística Ant Colony Optimization
│   └── ant.py                # Agente hormiga para ACO
│
├── gui/
│   ├── SUPPAI.py             # Interfaz gráfica principal (Tkinter)
│   ├── SUPPAI_support.py     # Lógica de soporte de la GUI y clase Optimizer
│   └── observer.py           # Patrón Observer para actualización de la GUI
│
├── db/
│   ├── database.py           # Conexión y operaciones sobre PostgreSQL
│   ├── queries.py            # Consultas SQL parametrizadas
│   ├── config.py             # Lectura de configuración de la base de datos
│   ├── write_csv.py          # Escritura de conjuntos en archivos CSV
│   └── database.ini          # Configuración de conexión (host, puerto, usuario, etc.)
│
├── experiments/
│   ├── initial_x/            # Estrategias para obtener la solución inicial X
│   ├── neighborhood/         # Funciones de generación de vecindad
│   ├── aco/                  # Experimentos específicos de ACO
│   ├── random_restart/       # Experimentos de Random Restart
│   └── test/                 # Scripts de prueba y validación
│
├── anims/
│   ├── aco_evol.py           # Animación de la evolución del ACO
│   ├── hc_evol.py            # Animación de la evolución del Hill Climbing
│   └── rr_evol.py            # Animación de la evolución del Random Restart
│
├── config/
│   └── data_creation_config.ini  # Parámetros para la generación de datos de entrada
│
└── LICENSE
```

---

## Requisitos

- Python 3.10+
- PostgreSQL 14+
- Paquetes Python (instalar con `pip`):

```
psycopg[binary]
pandas
numpy
matplotlib
tkinter   # Incluido en la instalación estándar de Python
```

---

## Instalación y configuración

### 1. Clonar el repositorio

```bash
git clone https://github.com/pps-ungs/supply-chain.git
cd supply-chain
```

### 2. Instalar dependencias

```bash
pip install psycopg[binary] pandas numpy matplotlib
```

### 3. Configurar la base de datos

Editar el archivo `db/database.ini` con las credenciales de PostgreSQL:

```ini
[supply_chain]
host     = localhost
port     = 5432
user     = postgres
password = tu_contraseña
dbname   = supply_chain
sslmode  = disable

[postgres]
host     = localhost
port     = 5432
user     = postgres
password = tu_contraseña
dbname   = postgres
sslmode  = disable
```

---

## Uso

### Interfaz gráfica (GUI)

La aplicación incluye una interfaz gráfica construida con **Tkinter** llamada **SUPPAI**.

```bash
cd gui
python SUPPAI_support.py
```

La GUI permite:

1. **Conectar a la base de datos** mediante un archivo `.ini` de configuración (menú `File → Connect to database...`).
2. **Seleccionar la heurística** a ejecutar (menú `Heuristics`):
   - Hill Climbing
   - Random Restart
   - Ant Colony Optimization
3. **Configurar los parámetros** del algoritmo seleccionado en el panel izquierdo.
4. **Ejecutar** la optimización con el botón `Run` y observar los resultados en tiempo real en el panel derecho.
5. Una **barra de progreso** indica el avance de la ejecución.

### Ejecución por línea de comandos

Desde la raíz del proyecto:

```bash
python main.py
```

Se solicitará una acción sobre la base de datos:

- `c` — Crear la base de datos desde los archivos CSV en `db/data/sets/`.
- `t` — Restaurar la base de datos desde un dump SQL en `db/data/dumps/`.
- `r` — Leer la base de datos existente.

A continuación, se ejecutan secuencialmente los tres algoritmos (ACO, Hill Climbing y Random Restart) con los parámetros definidos en `main.py`, mostrando los resultados en consola.

**Ejemplo de salida:**

```
################################################################################
    Experiment **ANT COLONY OPTIMIZATION**
--------------------------------------------------------------------------------
PARAMETERS
    alpha: 0.5, beta: 3.0, rho: 0.1, num_prod_levels: 200
--------------------------------------------------------------------------------
RESULTS
                X: [45230. 61800. 33120. 58900.]
                Z: 8742315.23
           Margin: 9150000.00
             pStk: 85000.00
             pDIn: 120000.00
            CTf2s: 95000.00
            CTs2p: 107684.77
       Iterations: 1000
             Time: 42.7
Halting condition: Max iterations reached
################################################################################

################################################################################
    Experiment **HILL CLIMBING**
--------------------------------------------------------------------------------
PARAMETERS
    step: 936, initial_X: [58000, 62000, 41000, 55000], max_iterations_allowed: 45
--------------------------------------------------------------------------------
RESULTS
                X: [58936, 62936, 41936, 55936]
                Z: 8801042.10
           Margin: 9210000.00
             pStk: 72000.00
             pDIn: 98000.00
            CTf2s: 130000.00
            CTs2p: 108957.90
       Iterations: 12
             Time: 89.3
Halting condition: Stuck in local optimum
################################################################################

################################################################################
    Experiment **RANDOM RESTART**
--------------------------------------------------------------------------------
PARAMETERS
    step: 936, max_iterations_allowed: 45
--------------------------------------------------------------------------------
RESULTS
                X: [61000, 70000, 38000, 52000]
                Z: 8834500.75
           Margin: 9250000.00
             pStk: 68000.00
             pDIn: 91000.00
            CTf2s: 145000.00
            CTs2p: 110499.25
       Iterations: 38
             Time: 134.6
Halting condition: Maximum loops without improvement
################################################################################
```

### Generación de datos de entrada

Para generar un conjunto de datos sintético nuevo y guardarlo en CSV:

```bash
python input_generator.py
```

Los parámetros se configuran en `config/data_creation_config.ini`:

```ini
[sets]
number_of_fabrication_centers  = 4
number_of_distribution_centers = 10
number_of_points_of_sale       = 50

[scenarios]
number_of_scenarios = 500
mean_demand         = 678
std_dev_demand      = 170
```

Los archivos generados se guardan en `db/data/conjuntos/`.

---

## Base de datos

El sistema utiliza **PostgreSQL** para almacenar los datos de la cadena de distribución. Las tablas son:

| Tabla                     | Descripción                                      |
|---------------------------|--------------------------------------------------|
| `centro_de_fabricacion`   | Centros de fabricación (nombre, datos)           |
| `centro_de_distribucion`  | Centros de distribución (nombre, datos)          |
| `punto_de_venta`          | Puntos de venta (nombre, datos)                  |
| `escenario`               | Escenarios de demanda (nombre, datos en JSONB)   |

Se puede hacer un backup de la base de datos en `db/data/dumps/supply-chain-dump.sql` durante la creación, y restaurarlo en cualquier momento.

---

## Experimentos y animaciones

El directorio `experiments/` contiene scripts para realizar experimentos comparativos entre algoritmos, variando parámetros y analizando resultados.

El directorio `anims/` contiene scripts que generan animaciones (`.gif`) de la **evolución del valor objetivo** a lo largo de las iteraciones de cada algoritmo, consultando el historial almacenado en la base de datos. Requieren `matplotlib` con el backend `TkAgg`.

```bash
python anims/aco_evol.py   # Evolución del ACO
python anims/hc_evol.py    # Evolución del Hill Climbing
python anims/rr_evol.py    # Evolución del Random Restart
```

---

## Autores y licencia

**Autores**: **Ebertz** (<a href="https://github.com/xebertz">@xebertz</a>), **Rondelli** (<a href="https://github.com/rondelli">@rondelli</a>), **Soria** (<a href="https://github.com/LuciaSoria5">@LuciaSoria5</a>).

Este proyecto está bajo la licencia **BSD 3-Clause**. Ver el archivo [LICENSE](LICENSE) para más detalles.
