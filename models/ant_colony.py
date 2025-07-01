import numpy as np
from ant import Ant
from models.model import Model

class AntColony(Model):
    ########################################################################
    # Colonia de hormigas
    #
    # F: centros de fabricación
    # S: centros de distribución
    # P: puntos de venta
    # E: escenarios
    ### Parámetros del algoritmo de colonia de hormigas
    # alpha: importancia del rastro de feromona (usualmente entre 0 y 1)
    # beta: importancia de la información heurística (usualmente > 1)
    # rho: tasa de evaporación de feromona (usualmente entre 0 y 1)
    # Q: constante para la actualización de feromona
    # 
    ### Devuelve un diccionario con los siguientes elementos:
    # 1. "X": mejor solución encontrada,
    # 2. "Z": mejor valor de la función objetivo encontrado
    # 3. "margin": margen de ganancia encontrado,
    # 4. "pStk": penalidad por exceso de stok,
    # 5. "pDIn": penalidad por demanda insatisfecha,
    # 6. "CTf2s": costo de transporte de fábricas a centros de distribución,
    # 7. "CTs2p": costo de transporte de centros de distribución a puntos de venta,
    # 8. "halting_condition": criterio de parada. En este modelo, sólo "Max iterations reached",
    # 9. "iterations": cantidad de iteraciones realizadas. En este modelo, la recibida por parámetro,
    # 10. "history_Z": historial de resultados de Z
    # 10. "history_X": historial de resultados de X
    def __init__(self, F, S, P, E, alpha=3.0, beta=1.0, rho=0.01, Q=100.0, tau_min=0.01, tau_max=10.0, num_prod_levels=500):
        super().__init__(F, S, P, E) 
        
        self.alpha = alpha
        self.beta = beta
        self.rho = rho
        self.Q = Q
        self.tau_min = tau_min
        self.tau_max = tau_max
        self.num_factories = len(self.F)
        self.num_prod_levels = num_prod_levels
        
        Z_best_expected = 8600000.0 # Valor de referencia
        
        pheromone_max_scale = 1000000
        self.Q = Q if Q is not None else pheromone_max_scale / Z_best_expected
        self.tau_max = tau_max if tau_max is not None else pheromone_max_scale
        self.tau_min = tau_min if tau_min is not None else self.tau_max * 0.0000001

        if self.tau_min <= 0:
            self.tau_min = 1e-6 

        self.pheromones = np.ones((self.num_factories, self.num_prod_levels)) * self.tau_max
        self.best_solution_X = None
        self.best_solution_Z = float('-inf')        
        self.best_margin = 0
        self.best_pStk = 0
        self.best_pDIn = 0
        self.best_CTf2s = 0
        self.best_CTs2p = 0
        
    def solve(self, num_ants=10, max_iterations=200):
        ant_colony = []
        for i in range(num_ants):
            ant_colony.append(Ant(i, self.F, self.S, self.P, self.E, self.num_prod_levels, self)) 
        
        history_Z = []
        history_X = []
        
        # print("[info] Starting Ant Colony optimization...")

        for _ in range(max_iterations):
            solutions_this_iteration = [] 
            
            # 1. Cada hormiga construye una solución
            for ant in ant_colony:
                X_ant_indices, X_ant_real_values, Z_ant, details_ant = ant.build_solution(self.pheromones, self.alpha, self.beta)
                solutions_this_iteration.append({
                    "X_indices": X_ant_indices,
                    "X_real_values": X_ant_real_values,
                    "Z": Z_ant, 
                    "details": details_ant,
                    "ant_id": ant.id
                })
                
                # 2. Actualizar la mejor solución 
                if Z_ant > self.best_solution_Z:
                    self.best_solution_Z = Z_ant
                    self.best_solution_X = X_ant_real_values
                    self.best_margin = details_ant['margin']
                    self.best_pStk = details_ant['pStk']
                    self.best_pDIn = details_ant['pDIn']
                    self.best_CTf2s = details_ant['CTf2s']
                    self.best_CTs2p = details_ant['CTs2p']
                    self.notify_observers([ self.best_solution_X, self.best_solution_Z, self.best_margin, self.best_pStk, self.best_pDIn, self.best_CTf2s, self.best_CTs2p, max_iterations ])

            # 3. Evaporación de feromonas
            self.pheromones = (1 - self.rho) * self.pheromones

            # 4. Actualización de feromonas
            # Solo la mejor hormiga (o las mejores) deposita feromonas.
            current_best_ant_sol = max(solutions_this_iteration, key=lambda sol: sol['Z'])
            
            # Calcular la cantidad de feromona a depositar.
            delta_tau_value = self.Q * current_best_ant_sol["Z"]
            
            # Depositar feromona en las aristas correspondientes a la solución de la mejor hormiga
            for i in range(self.num_factories):
                prod_level_index = current_best_ant_sol["X_indices"][i] 
                self.pheromones[i, prod_level_index] += delta_tau_value
            
            self.pheromones = np.clip(self.pheromones, self.tau_min, self.tau_max)
            
            # Registrar la mejor solución
            history_Z.append(self.best_solution_Z)
            history_X.append(self.best_solution_X.tolist())

            # For debugging:
            # if (iteration + 1) % 10 == 0 or iteration == 0:
            #     print(f"Iteration {iteration+1}/{max_iterations} - Best Z so far: {self.best_solution_Z:.2f}, X: {self.best_solution_X}")
            #     print(f"Pheromones sum: {np.sum(self.pheromones):.2f}")

        halting_condition = "Max iterations reached"
        
        return {
            "X": self.best_solution_X,
            "Z": self.best_solution_Z,
            "margin": self.best_margin,
            "pStk": self.best_pStk,
            "pDIn": self.best_pDIn,
            "CTf2s": self.best_CTf2s,
            "CTs2p": self.best_CTs2p,
            "halting_condition": halting_condition,
            "iterations": max_iterations,
            "history_Z": history_Z,
            "history_X": history_X
        }
