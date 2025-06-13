import numpy as np

class Ant:
    def __init__(self, id, F, S, P, E, num_production_levels, model_instance):
        self.id = id
        self.F = F 
        self.S = S 
        self.P = P 
        self.E = E 
        self.num_production_levels = num_production_levels
        self.model = model_instance 
        
        # Definir los niveles de producción reales para cada fábrica
        self.actual_prod_levels = {}
        for f_idx in range(len(self.F)):
            min_prod = 0 
            max_prod = 100000 
            self.actual_prod_levels[f_idx] = np.linspace(min_prod, max_prod, self.num_production_levels)

    def build_solution(self, pheromones, alpha, beta):
        self.solution_X_indices = np.zeros(len(self.F), dtype=int) 
        self.solution_X_real_values = np.zeros(len(self.F)) 

        for f_idx in range(len(self.F)):
            probabilities = self._calculate_probabilities(f_idx, pheromones, alpha, beta)
            
            chosen_level_index = np.random.choice(self.num_production_levels, p=probabilities)
            self.solution_X_indices[f_idx] = chosen_level_index
            self.solution_X_real_values[f_idx] = self.actual_prod_levels[f_idx][chosen_level_index]
            
        
        # Obtenemos los valores detallados para el retorno
        margin, pStk, pDIn, CTf2s, CTs2p = self.model.get_objective_function_values(
            self.F, self.S, self.P, self.E, self.solution_X_real_values.tolist()
        )
        
        # Calculamos el Z final
        self.solution_Z = self.model.objective_function(margin, pStk, pDIn, CTf2s, CTs2p)
        
        self.details = {
            "margin": margin,
            "pStk": pStk,
            "pDIn": pDIn,
            "CTf2s": CTf2s,
            "CTs2p": CTs2p
        }
        
        return self.solution_X_indices, self.solution_X_real_values, self.solution_Z, self.details

    def _calculate_probabilities(self, factory_index, pheromones, alpha, beta):
        heuristic_info = np.zeros(self.num_production_levels)
        
        # Calcular la demanda promedio total
        total_avg_demand = 0
        for scenario_demands_dict in self.model.get_demand_per_point_of_sale(self.E):
            total_avg_demand += sum(scenario_demands_dict.values())
        
        avg_demand_per_factory = total_avg_demand / len(self.F)

        for k in range(self.num_production_levels):
            prod_val = self.actual_prod_levels[factory_index][k]
            
            # Heurística: Favor al nivel de producción que se acerca a la demanda promedio esperada
            # para esta fábrica. La penalización aumenta cuanto más lejos esté.
            deviation = abs(prod_val - avg_demand_per_factory)
            heuristic_info[k] = 1.0 / (deviation + 1.0) 
            
            # Para evitar problemas numéricos si la heurística es 0
            if heuristic_info[k] < 1e-6:
                heuristic_info[k] = 1e-6 

        # Término de feromona ($\tau$)
        pheromone_term = pheromones[factory_index, :] ** alpha
        
        # Término heurístico ($\eta$)
        heuristic_term = heuristic_info ** beta
        
        # Calcular el numerador de la probabilidad
        numerator = pheromone_term * heuristic_term
        
        denominator = np.sum(numerator)
        
        if denominator == 0:
            # Si el denominador es cero (ej. todas las heurísticas son 0 o feromonas son 0),
            # asigna probabilidades uniformes para permitir exploración.
            return np.ones(self.num_production_levels) / self.num_production_levels
        
        probabilities = numerator / denominator
        
        # Asegurarse de que la suma de probabilidades sea 1 (por errores de punto flotante)
        probabilities /= np.sum(probabilities)
        return probabilities
