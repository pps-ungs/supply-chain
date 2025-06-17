import numpy as np

class Ant:
    def __init__(self, id, F, S, P, E, num_prod_levels, model_instance):
        self.id = id
        self.F = F 
        self.S = S 
        self.P = P 
        self.E = E 
        self.num_prod_levels = num_prod_levels
        self.model = model_instance 
        self.actual_prod_levels = {}
        for f_idx in range(len(self.F)):
            min_prod = 0 
            max_prod = 100000 
            self.actual_prod_levels[f_idx] = np.linspace(min_prod, max_prod, self.num_prod_levels)

    def build_solution(self, pheromones, alpha, beta):
        self.solution_X_indices = np.zeros(len(self.F), dtype=int) 
        self.solution_X_real_values = np.zeros(len(self.F)) 

        for f_idx in range(len(self.F)):
            probabilities = self._calculate_probabilities(f_idx, pheromones, alpha, beta)
            
            chosen_level_index = np.random.choice(self.num_prod_levels, p=probabilities)
            self.solution_X_indices[f_idx] = chosen_level_index
            self.solution_X_real_values[f_idx] = self.actual_prod_levels[f_idx][chosen_level_index]
            
        
        margin, pStk, pDIn, CTf2s, CTs2p = self.model.get_objective_function_values(
            self.F, self.S, self.P, self.E, self.solution_X_real_values.tolist()
        )
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
        heuristic_info = np.zeros(self.num_prod_levels)
        
        for k in range(self.num_prod_levels):
            heuristic_info[k] = 1.0
            
            if heuristic_info[k] < 1e-6:
                heuristic_info[k] = 1e-6

        pheromone_term = pheromones[factory_index, :] ** alpha
        
        heuristic_term = heuristic_info ** beta
        
        numerator = pheromone_term * heuristic_term
        
        denominator = np.sum(numerator)
        
        if denominator == 0:
            return np.ones(self.num_prod_levels) / self.num_prod_levels
        
        probabilities = numerator / denominator
        
        probabilities /= np.sum(probabilities)
        return probabilities