from Polygones_package import DemiPlan
import numpy as np
from Polygones_package.Vertex import Vertex
import time
import matplotlib.pyplot as plt


def get_list_polygones(polygone, n):
    res = [polygone]
    for i in range(n - 1):
        res.append(Vertex(res[-1]).translate((i + 2, i + 2)))
    return res


def insert_all_polygones(plan, polygones):
    for polygone in polygones:
        plan.insert_polygone(polygone)


def time_execution_insertion(plan, polygone):
    start_time = time.time()
    for i in range(50):
        plan.insert_polygone(polygone)
    return round((time.time() - start_time)/50, 5)


def get_list_times(polygone, list_n):
    time_executions = []
    for n in list_n:
        plan = DemiPlan()
        polygones = get_list_polygones(polygone, n)
        # On crée un plan de taille n-1 avant d'insérer le polygone
        insert_all_polygones(plan, polygones[:-1])
        time_executions.append(time_execution_insertion(plan, polygones[-1]))
    return time_executions


if __name__ == '__main__':
    # Check :
    plan = DemiPlan()
    L1 = np.array(((1, 1), (1, 3), (3, 3), (3, 1)))
    polygone_12 = np.array(((1, 1), (1, 2), (1, 3), (2, 4),
                            (3, 4), (4, 4), (5, 3), (5, 2),
                            (4, 1), (3, 1), (2, 1), (1.5, 1.5)
                            ))
    # list_n = [10, 100, 1000, 10000, 20000, 30000]
    # list_n = [10, 100, 500, 1000, 2000, 5000, 7500, 10000]
    list_n = [1, 100, 500, 1000, 1500, 2000, 5000, 10000]
    time_executions = get_list_times(L1, list_n)
    print("4 Sommets : ")
    for n, execution_time in zip(list_n, time_executions):
        print(f" n = {n} --- {execution_time} seconds ---")

    plt.title("Temps d'éxecution en fonction "
              "du nombre de polygones dans la collection")
    plt.xlabel("Nombre d'élements dans la collection")
    plt.ylabel("Temps d'éxécution pour insérer un polygone")
    plt.plot(list_n, time_executions, color='red', label='Polygone à 4 sommets')

    print("12 Sommets : ")
    time_executions = get_list_times(polygone_12, list_n)
    for n, execution_time in zip(list_n, time_executions):
        print(f" n = {n} --- {execution_time} seconds ---")
    plt.plot(list_n, time_executions, color='blue',
             label="Polygone à 12 sommets")

    plt.legend(loc="upper left")
    plt.savefig("times.png")
