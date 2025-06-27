import os
import sys
import inspect
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../models/')))

class HeuristicTestHelper:
    def solve(self, model, **kwargs) -> dict:

        initial_time = time.time()

        result = self.call_with_non_default_params(model.solve, **kwargs)
        actual_time = time.time() - initial_time

        X = result.get("X")
        Z = result.get("Z")
        halting_condition = result.get("halting_condition", "unknown")

        data = {
            "X": X,
            "Z": Z,
            "time": actual_time,
            "halting_condition": halting_condition
        }

        if "history" in result:
            data["history"] = result["history"]
            
        if "iterations" in result:
            data["iterations"] = result["iterations"]
            
        return data

    def call_with_non_default_params(self, func, **kwargs):
        sig = inspect.signature(func)
        filtered = {}
        for k, v in kwargs.items():
            param = sig.parameters.get(k)
            if param is None:
                continue
            if param.default is inspect.Parameter.empty or v != param.default:
                filtered[k] = v
        return func(**filtered)