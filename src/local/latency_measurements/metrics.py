from collections import defaultdict
from time import perf_counter
from functools import wraps
import json
import os
import threading
from abc import ABC, abstractmethod

lock = threading.Lock()


class Metrics(ABC):
    """
    Base class providing utilities for storing latency measurements.
    """

    @classmethod
    @abstractmethod
    def add_value(cls, name: str, value: float):
        """Records a latency measurement under the specified metric name."""
        pass

    @classmethod
    def measure(cls, name):
        """
        Decorator that measures the execution time of a function and records it
        under the specified metric name.
        """

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

    @classmethod
    def save_response_times_to_file(
        cls, scenario: str, values: list | dict, filename: str
    ):
        """
        Saves latency measurements to a JSON file.

        Existing data is preserved, and the measurements for the specified
        benchmark scenario are added or updated.

        :param scenario: Benchmark scenario name.
        :param values: Recorded latency measurements.
        :param filename: Output JSON file.
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
    """
    Collects latency measurements for the sequential benchmark.
    """

    round_latencies = defaultdict(float)
    global_latencies = []

    @classmethod
    def add_value(cls, name, value):
        cls.round_latencies[name] = value

    @classmethod
    def get_latencies(cls) -> list:
        """Returns all recorded latency measurements."""
        return list(cls.global_latencies)

    @classmethod
    def update_round_latencies(cls):
        """
        Stores the latency measurements collected during the current iteration.
        """
        cls.global_latencies.append(dict(cls.round_latencies))
        return


class ConcurrentMetrics(Metrics):
    """
    Collects latency measurements for the parallel benchmark.
    """

    global_latencies = defaultdict(list)

    @classmethod
    def add_value(cls, name, value):
        with lock:
            cls.global_latencies[name].append(value)

    @classmethod
    def get_latencies(cls) -> dict:
        """Returns all recorded latency measurements."""
        return dict(cls.global_latencies)
