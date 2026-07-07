import yaml

from logic.sequential import run_sequential_logic
from logic.threaded import run_threaded_logic


def validate_config(conf: dict):
    try:
        seq = conf["sequential"]
        conc = conf["concurrent"]

        seq["cycle"]
        seq["scenario"]

        cycle_by_service = conc["cycle_by_service"]
        cycle_by_service["detection"]
        cycle_by_service["identification"]
        conc["scenario"]

    except KeyError as e:
        raise RuntimeError(f"Missing configuration key: {e}") from e


def load_run_conf(file_path: str = "run_config.yaml") -> dict:
    with open(file_path, "r", encoding="utf-8") as f:
        conf = yaml.safe_load(f)

    if not isinstance(conf, dict):
        raise RuntimeError("The running config could not be loaded.")

    validate_config(conf)
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
