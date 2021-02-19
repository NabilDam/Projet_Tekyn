from Polygones_package import DemiPlan
import numpy as np
from Polygones_package.Vertex import Vertex

if __name__ == '__main__':
    # Check :
    plan = DemiPlan()
    T1 = np.array(((1, 1), (1, 5), (2, 3)))
    T1_translated = Vertex(T1).translate((6, 7))
    T1_180 = Vertex(T1).rotate_180()
    T2 = np.array(((1, 0.1), (2, 0.1), (3, 3)))

    plan.insert_polygone(T1)
    plan.insert_polygone(T1)
    plan.insert_polygone(T1_translated)
    plan.insert_polygone(T1_180)

    plan.move_polygone(T1, (9, 8))

    plan.insert_polygone(T2)

    lowest_polygone = plan.pop_lowest_polygone()

    res = plan.get_polygones_between(7, 16)
    print(res)
    plan.visualize_polygones("./data/demi_plan.png")
