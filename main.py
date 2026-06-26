from src.car_logic_seq import run_sequential_logic
from src.car_logic_thread import run_threaded_logic


def main():
    print("--- Benchmark Tool ---")
    print("1. Version Séquentielle")
    print("2. Version Multithread")

    choix = input("Choisissez une version (1 ou 2) : ")

    if choix == "1":
        print("Lancement du mode séquentiel...\n")
        run_sequential_logic()
    elif choix == "2":
        print("Lancement du mode multithread...\n")
        run_threaded_logic()
    else:
        print("Choix invalide.")


if __name__ == "__main__":
    main()
