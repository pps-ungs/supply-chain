import random
import numpy as np 

# --- 1. Clase para los Parámetros del Algoritmo de Colonia de Hormigas (ACO) ---
class ACOParameters:
    def __init__(self, n_ants, n_iterations, evaporation_rate, alpha, beta, q_factor, initial_pheromone):
        """
        n_ants (int): Número de hormigas en cada iteración.
        n_iterations (int): Número total de iteraciones del algoritmo.
        evaporation_rate (float): Tasa de evaporación de las feromonas (rho).
        alpha (float): Peso de la importancia de las feromonas (alfa).
        beta (float): Peso de la importancia de la heurística (beta).
        q_factor (float): Factor de depósito de feromona (Q).
        initial_pheromone (float): Valor inicial de feromona en los caminos.
        """
        self.n_ants = n_ants
        self.n_iterations = n_iterations
        self.evaporation_rate = evaporation_rate
        self.alpha = alpha
        self.beta = beta
        self.q_factor = q_factor
        self.initial_pheromone = initial_pheromone


# --- 2. Clase para los Datos del Problema de Distribución ---
class ProblemData:
    def __init__(self, ki_F, kj_S, kk_P, scenarios, costs, capacities, revenues):
        """
        Inicializa los datos específicos de tu problema de red de distribución.

        Args:
            num_factories (int): Número de fábricas.
            num_cds (int): Número de centros de distribución.
            num_pvs (int): Número de puntos de venta.
            scenarios (list): Lista de 500 escenarios de demanda. Cada escenario es una lista
                              de demandas para cada punto de venta (ej: [dem_pv0, dem_pv1, ...]).
            costs (dict): Diccionario de costos:
                          - 'production_cost': list (costo unitario por fábrica)
                          - 'f_cd_trans_cost': list of lists (matriz de costos F->CD)
                          - 'cd_pv_trans_cost': list of lists (matriz de costos CD->PV)
                          - 'shortfall_penalty': float (penalidad por unidad de demanda no satisfecha)
                          - 'excess_stock_penalty': float (penalidad por unidad de stock sobrante)
            capacities (dict): Diccionario de capacidades:
                               - 'factory_capacity': list (capacidad máxima de producción por fábrica)
                               - 'cd_capacity': list (capacidad de almacenamiento por CD)
                               - 'pv_max_stock': list (stock máximo permitido en PV antes de penalidad)
            revenues (dict): Diccionario de ingresos:
                             - 'unit_price': float (precio de venta por unidad)
        """
        self.num_factories = ki_F
        self.num_cds = kj_S
        self.num_pvs = kk_P
        self.scenarios = scenarios
        self.costs = costs
        self.capacities = capacities
        self.revenues = revenues


# --- 3. Clase para Representar una Solución (Plan de Producción) ---
class DistributionSolution:
    def __init__(self, production_plan, factory_to_cd_plan, cd_to_pv_plan, net_profit):
        """
        Representa una solución encontrada por una hormiga o la mejor solución global.

        Args:
            production_plan (dict): Plan de producción por fábrica {factory_id: units_produced}.
            factory_to_cd_plan (dict): Plan de envío F->CD (resultado de la heurística de distribución).
            cd_to_pv_plan (dict): Plan de envío CD->PV (resultado de la heurística de distribución).
            net_profit (float): Ganancia neta promedio calculada para este plan de producción.
        """
        self.production_plan = production_plan
        self.factory_to_cd_plan = factory_to_cd_plan
        self.cd_to_pv_plan = cd_to_pv_plan
        self.net_profit = net_profit


# --- 4. Clase Principal del Optimizador de Colonia de Hormigas ---
class AntColonyOptimizerProduction:
    def __init__(self, problem_data: ProblemData, parameters: ACOParameters):
        """
        Inicializa el optimizador de Colonia de Hormigas para el problema de producción.

        Args:
            problem_data (ProblemData): Instancia con los datos del problema.
            parameters (ACOParameters): Instancia con los parámetros del algoritmo.
        """
        self.problem_data = problem_data
        self.parameters = parameters
        
        # Define los posibles niveles de producción discretos para cada fábrica.
        # Por ejemplo, de 0 a la capacidad máxima, en pasos de 50 o 100 unidades.
        self.possible_production_levels_per_factory = self._define_production_levels()
        
        # Las feromonas se almacenan en una estructura que mapea fábricas a niveles de producción.
        self.pheromones_production = self._initialize_pheromones_production()
        
        # Almacena la mejor solución global encontrada hasta el momento.
        self.best_global_solution = None

    def _define_production_levels(self):
        """
        Define los niveles de producción discretos para cada fábrica.
        Ajusta el paso (e.g., 50) según la granularidad deseada para las decisiones de producción.
        """
        levels = []
        for i in range(self.problem_data.num_factories):
            # Crea una lista de niveles de producción desde 0 hasta la capacidad máxima, en pasos de 50.
            factory_levels = [x for x in range(0, self.problem_data.capacities['factory_capacity'][i] + 1, 50)]
            if 0 not in factory_levels: # Asegurar que 0 siempre sea una opción
                factory_levels.insert(0, 0)
            levels.append(factory_levels)
        return levels

    def _initialize_pheromones_production(self):
        """
        Inicializa la matriz de feromonas para cada fábrica y cada nivel de producción.
        """
        pheromones = []
        for i in range(self.problem_data.num_factories):
            factory_pheromones = [self.parameters.initial_pheromone] * len(self.possible_production_levels_per_factory[i])
            pheromones.append(factory_pheromones)
        return pheromones

    def _calculate_production_heuristic(self, factory_id: int, production_level_idx: int) -> float:
        """
        Calcula el valor heurístico para la decisión de producir un cierto nivel
        en una fábrica específica.

        Args:
            factory_id (int): ID de la fábrica.
            production_level_idx (int): Índice del nivel de producción en la lista de posibles.

        Returns:
            float: Valor heurístico.
        """
        production_level = self.possible_production_levels_per_factory[factory_id][production_level_idx]
        production_cost_per_unit = self.problem_data.costs['production_cost'][factory_id]

        if production_level == 0:
            # Desalentar la no producción a menos que sea realmente la mejor opción.
            # Puedes ajustar este valor si quieres un comportamiento diferente.
            return 0.001 
        
        # Ejemplo de heurística: Inversamente proporcional al costo total de producción.
        # +1e-6 para evitar división por cero si el costo total es 0.
        return 1.0 / (production_cost_per_unit * production_level + 1e-6) 

    def _construct_solution(self) -> DistributionSolution:
        """
        Una hormiga construye un plan de producción decidiendo cuántas unidades
        producir en cada fábrica, basándose en feromonas y heurística.
        """
        production_plan = {}
        for factory_id in range(self.problem_data.num_factories):
            probabilities = []
            for level_idx in range(len(self.possible_production_levels_per_factory[factory_id])):
                pheromone = self.pheromones_production[factory_id][level_idx]
                heuristic = self._calculate_production_heuristic(factory_id, level_idx)
                
                # Regla de transición probabilística: (feromona^alpha) * (heurística^beta)
                numerator = (pheromone ** self.parameters.alpha) * (heuristic ** self.parameters.beta)
                probabilities.append(numerator)

            total_probability = sum(probabilities)
            
            if total_probability == 0:
                # Si todas las probabilidades son cero, la hormiga elige un nivel aleatoriamente.
                # Esto puede ocurrir al inicio o si las feromonas/heurísticas son muy bajas.
                chosen_level_idx = random.randint(0, len(self.possible_production_levels_per_factory[factory_id]) - 1)
            else:
                normalized_probabilities = [p / total_probability for p in probabilities]
                # Usa random.choices para seleccionar un índice basado en las probabilidades
                chosen_level_idx = random.choices(range(len(normalized_probabilities)), weights=normalized_probabilities, k=1)[0]

            chosen_production_level = self.possible_production_levels_per_factory[factory_id][chosen_level_idx]
            production_plan[factory_id] = chosen_production_level

        # Una vez que la hormiga ha definido el plan de producción,
        # se calcula su ganancia neta promediada sobre todos los escenarios
        # resolviendo la distribución internamente con la heurística.
        net_profit = self._calculate_net_profit_averaged(production_plan)

        # Retorna la solución con el plan de producción y la ganancia neta.
        # Los planes F->CD y CD->PV son None porque no son decididos por la hormiga aquí.
        return DistributionSolution(production_plan, None, None, net_profit)

    def _calculate_net_profit_averaged(self, production_plan: dict) -> float:
        """
        Calcula la ganancia neta promedio de un plan de producción sobre todos los escenarios.
        """
        total_profit_sum = 0.0
        for scenario_demand in self.problem_data.scenarios:
            # Resuelve la distribución para el plan de producción y el escenario actual.
            _, _, profit_for_scenario = \
                self._solve_distribution_for_scenario(production_plan, scenario_demand)
            total_profit_sum += profit_for_scenario
        
        # Devuelve el promedio de las ganancias netas de todos los escenarios.
        return total_profit_sum / len(self.problem_data.scenarios)

    def _solve_distribution_for_scenario(self, production_plan: dict, scenario_demand: list) -> tuple:
        """
        HEURÍSTICA GREEDY para determinar la distribución F->CD y CD->PV,
        y calcular la ganancia neta para un escenario de demanda específico.

        Esta es una implementación que DEBES revisar y adaptar a la lógica exacta de tu negocio.
        """
        num_factories = self.problem_data.num_factories
        num_cds = self.problem_data.num_cds
        num_pvs = self.problem_data.num_pvs

        # --- FASE 1: Fábrica -> Centro de Distribución (F -> CD) ---
        # Inicialización de planes de envío y stock en CDs
        factory_to_cd_plan = {f_id: {cd_id: 0 for cd_id in range(num_cds)} for f_id in range(num_factories)}
        cd_stock = {cd_id: 0 for cd_id in range(num_cds)} # Stock que llega a cada CD
        
        # Copia de la producción inicial de cada fábrica para rastrear lo que queda por enviar
        f_remaining_production = production_plan.copy() 
        total_f_cd_cost = 0.0

        for f_id in range(num_factories):
            current_factory_production = f_remaining_production[f_id]
            if current_factory_production <= 0:
                continue

            # Ordenar los CDs por el costo de transporte más bajo desde la fábrica 'f_id'
            # y luego por capacidad restante (para CDs que puedan recibir más)
            sorted_cds = sorted(range(num_cds), 
                                key=lambda cd: (self.problem_data.costs['f_cd_trans_cost'][f_id][cd], 
                                                self.problem_data.capacities['cd_capacity'][cd] - cd_stock[cd]))

            for cd_id in sorted_cds:
                if current_factory_production <= 0: # Si la fábrica ya no tiene producción que enviar
                    break

                # Cantidad máxima que el CD puede recibir sin exceder su capacidad
                cd_max_receive = self.problem_data.capacities['cd_capacity'][cd_id] - cd_stock[cd_id]
                
                # Cantidad a enviar: lo mínimo entre la producción restante de la fábrica y lo que el CD puede recibir
                amount_to_send = min(current_factory_production, cd_max_receive)
                
                if amount_to_send > 0:
                    factory_to_cd_plan[f_id][cd_id] += amount_to_send
                    cd_stock[cd_id] += amount_to_send
                    total_f_cd_cost += amount_to_send * self.problem_data.costs['f_cd_trans_cost'][f_id][cd_id]
                    current_factory_production -= amount_to_send
        
        # --- FASE 2: Centro de Distribución -> Punto de Venta (CD -> PV) ---
        cd_to_pv_plan = {cd_id: {pv_id: 0 for pv_id in range(num_pvs)} for cd_id in range(num_cds)}
        
        # Copia de la demanda del escenario para rastrear lo que queda por satisfacer
        pv_demand_remaining = list(scenario_demand) 
        pv_stock_received = {pv_id: 0 for pv_id in range(num_pvs)} # Stock que realmente llega a cada PV
        total_cd_pv_cost = 0.0

        # Copia del stock de CD para no modificar el original durante la iteración
        current_cd_stock = cd_stock.copy()

        # Estrategia: Iterar por PVs, y para cada PV, intentar satisfacer su demanda
        # desde los CDs que tengan stock, priorizando los de menor costo de transporte.
        
        # Ordenar PVs por demanda descendente (para intentar satisfacer las más grandes primero)
        # O podrías ordenarlos por índice, o por costo de penalidad.
        sorted_pvs = sorted(range(num_pvs), key=lambda pv: pv_demand_remaining[pv], reverse=True)

        for pv_id in sorted_pvs:
            current_pv_demand = pv_demand_remaining[pv_id]
            if current_pv_demand <= 0:
                continue

            # Ordenar CDs por costo de transporte a este PV (ascendente)
            sorted_cds_for_pv = sorted(range(num_cds), 
                                       key=lambda cd: self.problem_data.costs['cd_pv_trans_cost'][cd][pv_id])

            for cd_id in sorted_cds_for_pv:
                if current_pv_demand <= 0: # Si la demanda del PV ya fue satisfecha
                    break
                if current_cd_stock[cd_id] <= 0: # Si el CD no tiene stock
                    continue

                # Cantidad a enviar: lo mínimo entre el stock disponible en el CD y la demanda restante del PV
                amount_to_send = min(current_cd_stock[cd_id], current_pv_demand)
                
                if amount_to_send > 0:
                    cd_to_pv_plan[cd_id][pv_id] += amount_to_send
                    pv_stock_received[pv_id] += amount_to_send
                    total_cd_pv_cost += amount_to_send * self.problem_data.costs['cd_pv_trans_cost'][cd_id][pv_id]
                    current_cd_stock[cd_id] -= amount_to_send
                    current_pv_demand -= amount_to_send
            
            # Actualizar la demanda restante del PV después de intentar satisfacerla
            pv_demand_remaining[pv_id] = current_pv_demand 

        # --- Cálculo de Ganancia Neta para el Escenario ---
        
        # 1. Ganancia por Ventas: Unidades realmente vendidas * precio unitario
        total_sales_revenue = 0.0
        for pv_id in range(num_pvs):
            # Las unidades vendidas son el mínimo entre lo que el PV recibió y su demanda inicial
            units_sold = min(pv_stock_received[pv_id], scenario_demand[pv_id])
            total_sales_revenue += units_sold * self.problem_data.revenues['unit_price']

        # 2. Costo de Producción: Suma de (unidades producidas por fábrica * costo unitario de producción)
        total_production_cost = 0.0
        for f_id, units in production_plan.items():
            total_production_cost += units * self.problem_data.costs['production_cost'][f_id]

        # 3. Penalidad por Demanda no Satisfecha (Shortfall Penalty)
        total_shortfall_penalty = 0.0
        for pv_id in range(num_pvs):
            # La demanda no satisfecha es lo que quedó de la demanda inicial después de las ventas
            shortfall = scenario_demand[pv_id] - min(pv_stock_received[pv_id], scenario_demand[pv_id])
            total_shortfall_penalty += shortfall * self.problem_data.costs['shortfall_penalty']

        # 4. Penalidad por Exceso de Stock (Excess Stock Penalty)
        total_excess_stock_penalty = 0.0
        
        # Exceso de stock en PVs (si un PV recibió más de lo que vendió, y el exceso supera su capacidad de stock)
        for pv_id in range(num_pvs):
            # Stock que quedó en el PV después de satisfacer la demanda
            remaining_pv_stock = max(0, pv_stock_received[pv_id] - scenario_demand[pv_id])
            # Penalizar solo si este stock restante excede la capacidad máxima del PV
            actual_excess_pv = max(0, remaining_pv_stock - self.problem_data.capacities['pv_max_stock'][pv_id])
            total_excess_stock_penalty += actual_excess_pv * self.problem_data.costs['excess_stock_penalty']

        # Exceso de stock en CDs (stock que quedó en los CDs y no pudo ser enviado a ningún PV)
        # current_cd_stock ya contiene el stock remanente en cada CD
        for cd_id in range(num_cds):
            total_excess_stock_penalty += current_cd_stock[cd_id] * self.problem_data.costs['excess_stock_penalty']


        # Cálculo final de la ganancia neta para este escenario
        net_profit_for_scenario = (
            total_sales_revenue -
            total_production_cost -
            total_f_cd_cost -
            total_cd_pv_cost -
            total_shortfall_penalty -
            total_excess_stock_penalty
        )

        return factory_to_cd_plan, cd_to_pv_plan, net_profit_for_scenario

    def _evaporate_pheromones(self):
        """
        Aplica la evaporación de feromonas a la matriz de producción.
        """
        for factory_id in range(self.problem_data.num_factories):
            for level_idx in range(len(self.pheromones_production[factory_id])):
                self.pheromones_production[factory_id][level_idx] *= (1 - self.parameters.evaporation_rate)

    def _update_global_pheromones(self, current_iteration_solutions: list):
        """
        Actualiza las feromonas basándose en las soluciones de la iteración actual
        y la mejor solución global.
        """
        # Encuentra la mejor solución de la iteración actual (la de mayor ganancia)
        best_current_iteration_solution = max(current_iteration_solutions, key=lambda s: s.net_profit)

        # Depósito de feromona. Si la ganancia es 0 o negativa, se maneja para evitar problemas.
        # Un valor muy bajo de ganancia puede llevar a un delta muy grande, por lo que se ajusta.
        if best_current_iteration_solution.net_profit > 0:
            delta_pheromone = self.parameters.q_factor / best_current_iteration_solution.net_profit
        else:
            # Si la ganancia es <= 0, deposita una cantidad fija o muy alta para "penalizar" (o evitar estancamiento)
            # Podrías ajustar este valor según la escala de tus ganancias.
            delta_pheromone = self.parameters.q_factor * 100 

        # La mejor solución de la iteración actual deposita feromonas en sus decisiones de producción
        for factory_id, production_level in best_current_iteration_solution.production_plan.items():
            # Encuentra el índice del nivel de producción elegido por esta solución
            if production_level in self.possible_production_levels_per_factory[factory_id]:
                level_idx = self.possible_production_levels_per_factory[factory_id].index(production_level)
                self.pheromones_production[factory_id][level_idx] += delta_pheromone
            # No hay 'else' porque production_level siempre debe estar en la lista de posibles.

        # Opcional: la mejor solución global también deposita feromona si es mejor que la actual
        if self.best_global_solution is not None and self.best_global_solution.net_profit > best_current_iteration_solution.net_profit:
             if self.best_global_solution.net_profit > 0:
                 delta_pheromone_global = self.parameters.q_factor / self.best_global_solution.net_profit
             else:
                 delta_pheromone_global = self.parameters.q_factor * 100

             for factory_id, production_level in self.best_global_solution.production_plan.items():
                if production_level in self.possible_production_levels_per_factory[factory_id]:
                    level_idx = self.possible_production_levels_per_factory[factory_id].index(production_level)
                    self.pheromones_production[factory_id][level_idx] += delta_pheromone_global

    def optimize(self) -> DistributionSolution:
        """
        Ejecuta el proceso de optimización de Colonia de Hormigas.
        """
        for iteration in range(self.parameters.n_iterations):
            current_iteration_solutions = []
            # Cada hormiga construye una solución (plan de producción)
            for _ in range(self.parameters.n_ants):
                solution = self._construct_solution()
                current_iteration_solutions.append(solution)

            # Evaporación y actualización de feromonas
            self._evaporate_pheromones()
            self._update_global_pheromones(current_iteration_solutions)

            # Actualiza la mejor solución global si se encontró una mejor en esta iteración
            best_current_iteration_solution = max(current_iteration_solutions, key=lambda s: s.net_profit)
            if self.best_global_solution is None or best_current_iteration_solution.net_profit > self.best_global_solution.net_profit:
                self.best_global_solution = best_current_iteration_solution

            print(f"Iteración {iteration+1}: Mejor ganancia actual = {self.best_global_solution.net_profit:.2f}")

        return self.best_global_solution


# --- Bloque Principal para la Ejecución (main) ---
if __name__ == "__main__":
    # --- Definir los datos de tu problema ---
    # AJUSTA ESTOS VALORES A TUS DATOS REALES
    num_factories = 2
    num_cds = 2
    num_pvs = 3

    # Costos: Debes asegurarte de que las dimensiones de las matrices coincidan con num_factories, num_cds, num_pvs.
    costs = {
        'production_cost': [10, 12],  # Costo por unidad de producción en Fábrica 0, Fábrica 1
        # Matriz de costos de transporte Fábrica a CD: [Fábrica][CD]
        'f_cd_trans_cost': [
            [1.0, 2.0],  # Costos de F0 a CD0, CD1
            [3.0, 1.5]   # Costos de F1 a CD0, CD1
        ],
        # Matriz de costos de transporte CD a PV: [CD][PV]
        'cd_pv_trans_cost': [
            [0.5, 0.8, 1.0],  # Costos de CD0 a PV0, PV1, PV2
            [0.7, 0.6, 0.9]   # Costos de CD1 a PV0, PV1, PV2
        ],
        'shortfall_penalty': 50.0, # Penalidad por unidad de demanda no satisfecha
        'excess_stock_penalty': 5.0 # Penalidad por unidad de stock sobrante en PV o CD
    }

    # Capacidades y Límites:
    capacities = {
        'factory_capacity': [1000, 1200], # Capacidad máxima de producción de cada fábrica
        'cd_capacity': [800, 900],        # Capacidad máxima de almacenamiento de cada CD
        'pv_max_stock': [200, 250, 300]   # Stock máximo permitido en cada PV antes de penalidad
    }

    # Ingresos:
    revenues = {'unit_price': 60.0} # Precio de venta por unidad

    # Escenarios de demanda: Lista de 500 escenarios, cada uno es una lista de demandas para los PVs.
    # Aquí se generan 500 escenarios aleatorios de ejemplo.
    # En un caso real, cargarías tus 500 escenarios predefinidos.
    num_scenarios = 500
    scenarios = [np.random.randint(20, 100, size=num_pvs).tolist() for _ in range(num_scenarios)]

    # Crea la instancia de ProblemData con tus datos
    problem_data = ProblemData(num_factories, num_cds, num_pvs, scenarios, costs, capacities, revenues)

    # --- Definir los parámetros del algoritmo ACO ---
    # Estos valores pueden necesitar ser ajustados mediante experimentación (tuning)
    # para tu problema específico para obtener los mejores resultados.
    parameters = ACOParameters(
        n_ants=10,             # Cantidad de hormigas en cada iteración
        n_iterations=200,      # Número total de iteraciones del algoritmo
        evaporation_rate=0.05, # Tasa de evaporación de feromonas (rho). 0.05 significa 5% de evaporación.
        alpha=1.0,             # Importancia relativa de las feromonas
        beta=2.0,              # Importancia relativa de la heurística (solo para producción en este caso)
        q_factor=10000.0,      # Factor de depósito de feromona. Ajusta según la escala de tus ganancias.
        initial_pheromone=1.0  # Valor inicial de feromona en todos los caminos
    )

    # --- Ejecutar el optimizador ACO ---
    aco_optimizer = AntColonyOptimizerProduction(problem_data, parameters)
    print("Iniciando optimización de Colonia de Hormigas...")
    best_solution = aco_optimizer.optimize()

    # --- Mostrar los resultados finales ---
    print("\n--- Resultados Finales de la Optimización ---")
    print(f"Mejor plan de producción encontrado: {best_solution.production_plan}")
    print(f"Máxima ganancia neta promedio obtenida: {best_solution.net_profit:.2f}")

    # Si quieres ver un ejemplo de cómo se distribuiría para la mejor solución encontrada
    # bajo un escenario de demanda promedio (o cualquier otro escenario representativo):
    avg_demand_scenario = [sum(s[i] for s in scenarios) / len(scenarios) for i in range(num_pvs)]
    print(f"\nDemanda promedio de los PVs (ejemplo para distribución): {avg_demand_scenario}")

    # Calcula el plan de distribución para la mejor solución de producción y la demanda promedio
    final_f_cd_plan, final_cd_pv_plan, _ = aco_optimizer._solve_distribution_for_scenario(
        best_solution.production_plan, avg_demand_scenario
    )
    print(f"Ejemplo de plan Fábrica -> CD (para demanda promedio): {final_f_cd_plan}")
    print(f"Ejemplo de plan CD -> PV (para demanda promedio): {final_cd_pv_plan}")