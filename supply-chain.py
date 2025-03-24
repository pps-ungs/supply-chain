import psycopg

with psycopg.connect("dbname=coso user=postgres") as conn:
    with conn.cursor() as cur:
        cur.execute("""
            create table if not exists escenario (
                id serial primary key,
                nombre text,
                data text)
            """)

        cur.execute(
            "insert into escenario (nombre, data) values (%s, %s)",
            ("Viva Perón", "muchas ventas"))

        cur.execute("select * from escenario;")
        cur.fetchone()

        for record in cur:
            print(record)

        conn.commit()

def generar_escenarios() -> set:
    return set()

# Función objetivo
# vtas: monto de ventas esperadas
# pStk: penalidad esperada por stock almacenado en los puntos de venta
# pDIn: penalidad esperada por demanda insatisfecha en los puntos de venta
def z(vtas: float, pStk: float, pDIn: float) -> float:
    return vtas - pStk - pDIn

def maximizar(z: callable[[float, float, float], float]) -> float:
    return 0

for escenario in generar_escenarios():
    vtas = escenario['vtas']
    pStk = escenario['pStk']
    pDIn = escenario['pDIn']

print(maximizar(z))