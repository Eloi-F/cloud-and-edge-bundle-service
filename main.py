from src.car_logic_seq import run_sequential_logic
from src.car_logic_thread import run_threaded_logic


def main():
    """
    Entry point of the benchmark application.

    The user selects either the sequential or multithreaded execution mode.
    Each mode runs the benchmark with predefined parameters.
    """
    print("--- Benchmark Tool ---")
    print("1. Sequential Version")
    print("2. Multithreaded Version")

    choice = input("Choose a version (1 or 2): ")

    if choice == "1":
        print("Starting sequential mode...\n")
        run_sequential_logic(10, "bundle")
    elif choice == "2":
        print("Starting multithreaded mode...\n")
        cycle_by_service = {"detection": 50, "identification": 20}
        run_threaded_logic(cycle_by_service, "bundle")
    else:
        print("Invalid choice.")


if __name__ == "__main__":
    main()
