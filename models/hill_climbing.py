import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.model import Model
import experiments.neighborhood.neighborhood as neighborhood

class HillClimbing(Model):
    ########################################################################
    # Escalador de colinas
    #
    # F: centros de fabricación
    # S: centros de distribución
    # P: puntos de venta
    # E: escenarios
    #
    # step: tamaño del paso para la búsqueda local
    # epsilon: tolerancia para la convergencia, es un valor muy pequeño
    # max_iterations_allowed: número máximo de iteraciones permitidas, es un valor grande
    #
    # Devuelve un diccionario con los siguientes elementos:
    # 1. X: mejor solución encontrada
    # 2. Z: mejor valor de la función objetivo encontrado
    # 3. margin: margen de ganancia encontrado
    # 4. pStk: penalidad por exceso de stock
    # 5. pDIn: penalidad por demanda insatisfecha
    # 6. CTf2s: costo de transporte de fábricas a centros de distribución
    # 7. CTs2p: costo de transporte de centros de distribución a puntos de venta
    # 8. halting_condition: criterio de parada. Puede ser "Satisfactory solution found",
    #    "Maximum number of iterations" o "Stuck in local optimum"
    # 9. iterations: cantidad de iteraciones realizadas
    def solve(self, step=20, epsilon=1e-12, max_iterations_allowed=1e12, max_stuck_allowed: int = 1, initial_X = 0):
        F, S, P, E = self.F, self.S, self.P, self.E

        X_initial, Z_initial = initial_X, self.get_objective_value(F, S, P, E, initial_X) if initial_X != 0 else ([100 for _ in F], 0)

        X_current = X_initial
        Z_current = Z_initial
        Z_previous = Z_current

        it = 0
        stuck = 0

        ####################################################################
        # Criterios de parada
        Z_current_is_better = True
        limit_is_not_reached = True
        is_not_stuck = True
        ####################################################################

        while Z_current_is_better and limit_is_not_reached and is_not_stuck:
            neighbors = neighborhood.create_multi_change_neighbors(X_current, step, 64)
            evaluated_neighbors = [(n, self.get_objective_value(F, S, P, E, n)) for n in neighbors]

            # Evaluation of the neighbourhood
            best_n, best_z = neighborhood.greedy_selection_eval(evaluated_neighbors, Z_current)

            print(f"[info] Iteration {it}: current Z = {Z_current}, best neighbor Z = {best_z}")
            # Comparing the best solution with the current one
            if best_n is not None:
                X_current = best_n
                Z_previous = Z_current
                Z_current = best_z
                margin, pStk, pDIn, CTf2s, CTs2p = self.get_objective_function_values(F, S, P, E, X_current)
                self.notify_observers([ X_current, Z_current, margin, pStk, pDIn, CTf2s, CTs2p, it ])

            ################################################################
            # Criterios de parada
            #
            # 1. Número máximo de iteraciones:
            it += 1
            limit_is_not_reached = it < max_iterations_allowed
            #
            # 2. Estancamiento:
            if Z_current == Z_previous:
                stuck += 1
                print(f"[warning] stuck in local optimum {Z_current} for {stuck} iterations")
            elif Z_current > Z_previous:
                stuck = 0
                # 3. Mejora entre las iteraciones
                #
                # Si la mejora es mayor a epsilon, se considera que la
                # solución actual es mejor que la anterior, y se sigue
                # buscando.
                Z_current_is_better = abs(Z_current - Z_previous) > epsilon
            else: # Z_current < Z_previous
                # Este es el caso en el que la solución anterior es mejor.
                # Nosotros usamos greedy local search, por ende, no se
                # debería dar este caso. Pero si se da, es porque la
                # solución anterior es mejor que la actual.
                stuck = 0
                raise Exception(f"?previous objective value {Z_previous} is better than the current one {Z_current}")

            if Z_current < 0:
                print(f"[warning] current objective value is negative: {Z_current}")

            is_not_stuck = stuck < max_stuck_allowed
            ################################################################

        halting_condition = None
        if not Z_current_is_better:
            halting_condition = "Satisfactory solution found"
        elif not limit_is_not_reached:
            halting_condition = "Maximum number of iterations"
        elif not is_not_stuck:
            halting_condition = "Stuck in local optimum"

        margin, pStk, pDIn, CTf2s, CTs2p = self.get_objective_function_values(F, S, P, E, X_current)

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
