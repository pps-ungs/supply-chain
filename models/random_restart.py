import sys
import os
import random

from models.hill_climbing import HillClimbing

class RandomRestart(HillClimbing):

    def solve(self, step=20, epsilon=1e-12, max_iterations_allowed=1e12, max_stuck_allowed: int = 1, initial_X = None, max_loops_without_improvement = 10, max_restarts=10):
        random.seed(42)

        loops_without_improvement = 0
        amount_of_restarts = 0

        X = initial_X if initial_X is not None else [100 for _ in self.F]
        best_result = None

        while loops_without_improvement < max_loops_without_improvement and amount_of_restarts < max_restarts:
            X = [x + random.randint(0, 10000) for x in X]
            result = super().solve(step, epsilon, max_iterations_allowed, max_stuck_allowed, X)

            if result["Z"] is not None and result["Z"] > best_result["Z"] if best_result else True:
                best_result = result
                loops_without_improvement = 0
                print(f"[info] New best result found: Z = {result['Z']}, X = {result['X']}")
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