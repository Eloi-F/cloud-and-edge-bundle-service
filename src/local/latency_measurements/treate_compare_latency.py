import json
import matplotlib.pyplot as plt

def load_json(filename):
    with open(filename, 'r') as f:
        return json.load(f)

def save_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f)

def add_lists(list1, list2):
    if len(list1) != len(list2):
        raise ValueError("Les listes doivent avoir la même longueur")
    return [x + y for x, y in zip(list1, list2)]

def plot_list(data1, data2, data3):
    plt.figure(figsize=(10, 5))
    plt.plot(data1, marker='o', color='green', label="Edge")
    plt.plot(data2, marker='x', color='blue', label="Cloud")
    plt.plot(data3, marker='_', color='red', label='Bundle service')
    plt.title('Comparison of latencies')
    plt.xlabel('Number of requests')
    plt.ylabel('Latency in ms')
    plt.grid(True)
    plt.legend()
    plt.show()

def calcule_moyenne(listes):
    l = len(listes)
    results = []
    for j in range(100):
        value = 0
        for i in range(10):
            value += listes[i][j]
        value = value / 10
        results.append(value)
    return results


list1 = load_json('edge_response_latency.json')
list2 = load_json('edge2_response_latency.json')
list3 = load_json('cloud_response_latency.json')
list4 = load_json('cloud2_response_latency.json')
list5 = load_json('cloud_edge_response_latency.json')
list6 = load_json('cloud_edge2_response_latency.json')

try:

    result_list1 = add_lists(calcule_moyenne(list1), calcule_moyenne(list2))
    result_list2 = add_lists(calcule_moyenne(list3), calcule_moyenne(list4))
    result_list3 = add_lists(calcule_moyenne(list5), calcule_moyenne(list6))
except ValueError as e:
    print(f"Erreur : {e}")
    result_list1 = []
    result_list2 = []
    result_list3 = []

save_json(result_list1, 'result_file1.json')
save_json(result_list2, 'result_file2.json')
save_json(result_list3, 'result_file3.json')

plot_list(result_list1, result_list2, result_list3)

print(f"La nouvelle liste est sauvegardée dans result_file.json")
