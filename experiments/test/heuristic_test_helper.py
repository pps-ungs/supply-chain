import os
import sys
import inspect
import time
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../db/')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../models/')))

import db.config as dbconfig
import db.database as db


class HeuristicTestHelper:
    dbconfig = {}

    def solve(
            self,
            model,
            step: int = 20,
            initial_obj: tuple = (None, None),
            epsilon: float = 1e-12,
            max_iterations_allowed: int = 1e12,
            max_stuck_allowed: int = 1e3,
            loops_without_improvement = 10,
            max_restarts = 10
        ) -> dict:

        initial_time = time.time()

        solve_kwargs = {
            "step": step,
            "epsilon": epsilon,
            "max_iterations_allowed": max_iterations_allowed,
            "max_stuck_allowed": max_stuck_allowed,
            "initial_X": initial_obj[0],
            "loops_without_improvement": loops_without_improvement,
            "max_restarts": max_restarts
        }

        result = self.call_with_non_default_params(model.solve, **solve_kwargs)
        actual_time = time.time() - initial_time
        
        X = result["X"]
        Z = result["Z"]
        halting_condition = result.get("halting_condition", "unknown")

        return {
            "X": X,
            "Z": Z,
            "time": actual_time,
            "halting_condition": halting_condition
        }

    def call_with_non_default_params(self, func, **kwargs):
        sig = inspect.signature(func)
        filtered = {}
        for k, v in kwargs.items():
            param = sig.parameters.get(k)
            if param is None:
                continue  # ignora parámetros que no existen en la función
            if param.default is inspect.Parameter.empty or v != param.default:
                filtered[k] = v
        return func(**filtered)