from model import Model
from ant import Ant

class AntColony(Model):
    
    # Los valore de los siguientes parámetros se toman de la base de datos
    # F: centros de fabricación
    # S: centros de distribución
    # P: puntos de venta
    # E: escenarios
    # Devuelve un diccionario con los siguientes elementos:
    # 1. X: mejor solución encontrada
    # 2. Z: valor de la función objetivo para la mejor solución
    # 3. margin: margen de beneficio
    # 4. pStk: cantidad de producto en stock
    # 5. pDIn: cantidad de producto distribuido
    # 6. CTf2s: costo de transporte de fabricación a distribución
    # 7. CTs2p: costo de transporte de distribución a puntos de venta
    # 8. halting_condition: condición de parada
    # 9. iterations: número de iteraciones realizadas
    # TODO
    def solve(self, num_ants=100, max_iterations=1000):
        ant_colony = []
        for i in range(num_ants):
            ant_colony.append(Ant(i))

        for ant in ant_colony:
            # cualquiera
            ant.buscar_solucion(self.F, self.S, self.P, self.E)
            ant.update_pheromone(self.F, self.S, self.P, self.E)
            ant.update_best_solution(self.F, self.S, self.P, self.E)

        print("[info] Fake Starting Ant Colony optimization...")

        X_current = 626
        Z_current = 626
        margin = 626
        pStk = 626
        pDIn = 626
        CTf2s = 626
        CTs2p = 626
        halting_condition = 626
        it = 626

        return {
            "X": X_current,
            "Z": Z_current,
            "margin": margin,
            "pStk": pStk,
            "pDIn": pDIn,
            "CTf2s": CTf2s,
            "CTs2p": CTs2p,
            "halting_condition": halting_condition,
            "iterations": it
        }
