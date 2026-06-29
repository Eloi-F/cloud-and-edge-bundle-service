from src.car_logic_seq import run_sequential_logic
from src.car_logic_thread import run_threaded_logic


def main():
    print("--- Benchmark Tool ---")
    print("1. Version Séquentielle")
    print("2. Version Multithread")

    choix = input("Choisissez une version (1 ou 2) : ")

    if choix == "1":
        print("Lancement du mode séquentiel...\n")
        run_sequential_logic(10, "full_cloud")
    elif choix == "2":
        print("Lancement du mode multithread...\n")
        cycle_by_service = {"detection": 50, "identification": 20}
        run_threaded_logic(cycle_by_service, "full_cloud")
    else:
        print("Choix invalide.")


if __name__ == "__main__":
    main()
