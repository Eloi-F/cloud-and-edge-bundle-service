from collections import defaultdict
from time import perf_counter
from functools import wraps
import json


class Metrics:
    latencies = defaultdict(list)

    @classmethod
    def add_value(cls, name, value):
        cls.latencies[name].append(value)

    @classmethod
    def avg(cls, name):
        values = cls.latencies[name]
        return sum(values) / len(values)

    @classmethod
    def save_response_times_to_file(cls, filename="cloud_edge_response_latency.json"):
        """
        Save recorded latency measurements to a JSON file.
        """
        with open(filename, "w") as f:
            json.dump(cls.latencies, f)

        print(f"Temps de réponse sauvegardés dans {filename}")


def measure(name):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start = perf_counter()

            try:
                return func(*args, **kwargs)

            finally:
                Metrics.add_value(
                    name,
                    (perf_counter() - start) * 1000,
                )

        return wrapper

    return decorator
