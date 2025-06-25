import random

from models.hill_climbing import HillClimbing

class RandomRestart(HillClimbing):

    def solve(self, step=20, epsilon=1e-12, max_iterations_allowed=1e12, max_stuck_allowed: int = 1, max_loops_without_improvement = 10, max_restarts=10) -> dict :
        amount_of_restarts = 0
        loops_without_improvement = 0

        X = [100 for _ in self.F]
        best_result = None

        while loops_without_improvement < max_loops_without_improvement or amount_of_restarts < max_restarts:
            X = [random.randint(0, 100000) for _ in X]
            print(f"Restarting with X: {X}, amount_of_restarts: {amount_of_restarts}, loops_without_improvement: {loops_without_improvement}")
            
            result = super().solve(step, epsilon, max_iterations_allowed, max_stuck_allowed, X)

            if result["Z"] is not None and result["Z"] > best_result["Z"] if best_result else True:
                best_result = result
                loops_without_improvement = 0
            else:
                loops_without_improvement += 1
                amount_of_restarts += 1

        if loops_without_improvement >= max_loops_without_improvement:
            random_restart_halting_condition = "Maximum loops without improvement"
        else:
            random_restart_halting_condition = "Maximum number of restarts"

        best_result["halting_condition"] = random_restart_halting_condition
        best_result["amount_of_restarts"] = amount_of_restarts
        best_result["loops_without_improvement"] = loops_without_improvement
        return best_result
