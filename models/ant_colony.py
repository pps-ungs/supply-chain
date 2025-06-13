import numpy as np
from ant import Ant
from models.model import Model # Asegúrate de que ant.py esté en la misma carpeta o ruta

class AntColony(Model):
    # F: centros de fabricación
    # S: centros de distribución
    # P: puntos de venta
    # E: escenarios
    # Parámetros del algoritmo de colonia de hormigas
    # alpha: importancia del rastro de feromona (usualmente entre 0 y 1)
    # beta: importancia de la información heurística (usualmente > 1)
    # rho: tasa de evaporación de feromona (usualmente entre 0 y 1)
    # Q: constante para la actualización de feromona
    def __init__(self, F, S, P, E, alpha=1.0, beta=2.0, rho=0.1, Q=100.0, tau_min=0.01, tau_max=10.0):
        super().__init__(F, S, P, E) 
        
        self.alpha = alpha
        self.beta = beta
        self.rho = rho
        self.Q = Q
        
        # Parámetros para el sistema Max-Min Ant System (evitar estancamiento)
        self.tau_min = tau_min
        self.tau_max = tau_max

        self.num_factories = len(self.F)
        
        # Definir el número de niveles discretos para la producción.
        self.num_prod_levels = 100
        
        Z_best_expected = 8507422.0 # Valor de referencia
        
        # Calcular Q y tau_max basándose en Z_best_expected
        pheromone_max_scale = 10000
        
        # Si Q no se proporciona, lo calculamos
        self.Q = Q if Q is not None else pheromone_max_scale / Z_best_expected
        
        # Si tau_max no se proporciona, lo calculamos
        self.tau_max = tau_max if tau_max is not None else pheromone_max_scale # Usamos el valor objetivo como tau_max

        # Si tau_min no se proporciona, lo calculamos como una fracción de tau_max
        self.tau_min = tau_min if tau_min is not None else self.tau_max * 0.0001

        if self.tau_min <= 0:
            self.tau_min = 1e-6 

        # Inicialización de las feromonas con tau_max
        self.pheromones = np.ones((self.num_factories, self.num_prod_levels)) * self.tau_max
        
        # Mejor solución encontrada globalmente
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
        
        print("[info] Starting Ant Colony optimization...")

        for iteration in range(max_iterations):
            solutions_this_iteration = [] 
            
            # 1. Cada hormiga construye una solución
            for ant in ant_colony:
                X_ant_indices, X_ant_real_values, Z_ant, details_ant = ant.build_solution(self.pheromones, self.alpha, self.beta)
                solutions_this_iteration.append({
                    "X_indices": X_ant_indices,  # Los índices de los niveles de producción
                    "X_real_values": X_ant_real_values, # Los valores reales de producción
                    "Z": Z_ant, 
                    "details": details_ant,
                    "ant_id": ant.id
                })
                
                # 2. Actualizar la mejor solución global
                if Z_ant > self.best_solution_Z:
                    self.best_solution_Z = Z_ant
                    self.best_solution_X = X_ant_real_values
                    self.best_margin = details_ant['margin']
                    self.best_pStk = details_ant['pStk']
                    self.best_pDIn = details_ant['pDIn']
                    self.best_CTf2s = details_ant['CTf2s']
                    self.best_CTs2p = details_ant['CTs2p']

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
            
            # Registrar la mejor solución de esta iteración
            history_Z.append(self.best_solution_Z)

            if (iteration + 1) % 10 == 0 or iteration == 0:
                print(f"Iteration {iteration+1}/{max_iterations} - Best Z so far: {self.best_solution_Z:.2f}")
                # print(f"Pheromones sum: {np.sum(self.pheromones):.2f}") # Para depuración

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
            "history_Z": history_Z
        }
