from Polygones_package import DemiPlan
import numpy as np
from Polygones_package.Vertex import Vertex

if __name__ == '__main__':
    # Check :
    plan = DemiPlan()
    T1 = np.array(((1, 1), (1, 5), (2, 2)))
    T2 = np.array(((1, 2), (1, 5), (2, 3)))
    T3 = np.array(((1, 2), (1, 6), (2, 4)))
    T4 = np.array(((1, 2), (1, 5.5), (2, 3)))
    plan.insert_polygone(T1)
    plan.insert_polygone(T2)
    plan.insert_polygone(T3)
    print("----------------")
    plan.insert_polygone(T4)
    print(plan)