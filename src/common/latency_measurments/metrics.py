from collections import defaultdict
from time import perf_counter
from functools import wraps
import json
import os
import threading

lock = threading.Lock()


class Metrics:
    @classmethod
    def save_response_times_to_file(
        cls, scenario: str, values: list | dict, filename: str
    ):
        """
        Add or update recorded latency measurements to a JSON file.
        """
        data = {}

        if os.path.exists(filename):
            try:
                with open(filename, "r") as f:
                    data = json.load(f)
            except (json.JSONDecodeError, IOError):
                print(f"Warning: {filename} corrupted. Creating new file.")
                data = {}

        data[scenario] = values

        with open(filename, "w") as f:
            json.dump(data, f, indent=2)

        print(f"Data for '{scenario}' saved to {filename}")


class SeqMetrics(Metrics):
    latencies = defaultdict(float)

    @classmethod
    def add_value(cls, name, value):
        cls.latencies[name] = value

    @classmethod
    def get_current_round_latencies(cls) -> dict[str, float]:
        """
        Return the values of latency for the current 'round'
        """
        return cls.latencies

    @classmethod
    def measure(cls, name):
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                start = perf_counter()

                try:
                    return func(*args, **kwargs)

                finally:
                    cls.add_value(
                        name,
                        (perf_counter() - start) * 1000,
                    )

            return wrapper

        return decorator


class ConcurrentMetrics(Metrics):
    latencies = defaultdict(list)

    @classmethod
    def add_value(cls, name, value):
        with lock:
            cls.latencies[name].append(value)

    @classmethod
    def measure(cls, name):
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                start = perf_counter()

                try:
                    return func(*args, **kwargs)

                finally:
                    cls.add_value(
                        name,
                        (perf_counter() - start) * 1000,
                    )

            return wrapper

        return decorator
