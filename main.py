import yaml

from src.car_logic_seq import run_sequential_logic
from src.car_logic_thread import run_threaded_logic


def load_run_conf(file_path: str = "run_config.yaml"):
    with open(file_path, "r") as f:
        conf = yaml.safe_load(f)
    return conf


def main():
    """
    Entry point of the benchmark application.

    The user selects either the sequential or multithreaded execution mode.
    Each mode runs the benchmark with predefined parameters.
    """
    conf = load_run_conf()
    print("--- Benchmark Tool ---")
    print("1. Sequential Version")
    print("2. Multithreaded Version")

    choice = input("Choose a version (1 or 2): ")

    if choice == "1":
        print("Starting sequential mode...\n")

        seq_conf = conf["sequential"]
        run_sequential_logic(seq_conf["cycle"], seq_conf["scenario"])
    elif choice == "2":
        print("Starting multithreaded mode...\n")

        conc_conf = conf["concurrent"]
        run_threaded_logic(conc_conf["cycle_by_service"], conc_conf["scenario"])
    else:
        print("Invalid choice.")


if __name__ == "__main__":
    main()
