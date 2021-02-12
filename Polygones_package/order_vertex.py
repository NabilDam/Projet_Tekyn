import numpy as np
from .logging_type import logging


def permutation_vertex(vertex, index_min):
    part_1 = np.array([vertex[index_min]])
    part_2 = vertex[index_min + 1:]
    part_3 = vertex[:index_min]
    new_vertex = np.append(part_1, part_2, axis=0)
    new_vertex = np.append(new_vertex, part_3, axis=0)
    return new_vertex


def check_coords_id(coords):
    try:
        l = len(coords)
    except:
        logging.error(
            f" The coordinates must be in a list, tuple, set or array")
        raise

    if len(coords) != 2:
        raise ValueError("The coordinates must size of 2")

    if not type(coords[0]) in (float, int, np.float64, np.int_):
        raise TypeError("The coordinates must be float or int")

    if not type(coords[1]) in (float, int, np.float64, np.int_):
        raise TypeError("The coordinates must be float or int")
    return True


def check_coords(coords):
    check_coords_id(coords)
    if coords[1] <= 0:
        raise ValueError("y-axis must be > 0")
    return True


def check_vertex_is_conform(vertex):
    try:
        set_vertex = set(tuple(coords) for coords in vertex)
    except:
        logging.error("The coordinates must be in a list, tuple, set or array")
        raise

    if len(vertex) != len(set_vertex):
        logging.error("The polygone must contains "
                      "two size vertex with only differents points")
        raise
    return True


def check_all_coords(vertex):
    for coords in vertex:
        check_coords(coords)


def check_all_coords_id(vertex):
    for coords in vertex:
        check_coords_id(coords)


def order_polygone(vertex):
    check_vertex_is_conform(vertex)
    check_all_coords(vertex)
    vertex = np.array(vertex)

    y_list = vertex[:, 1]
    mins_y = np.where(y_list == y_list.min())[0]
    if len(mins_y) == 1:
        return permutation_vertex(vertex, mins_y[0])
    else:
        x_list = vertex[mins_y, 0]
        mins_x = np.where(x_list == x_list.min())[0]
        return permutation_vertex(vertex, mins_y[mins_x[0]])


def order_polygone_id(vertex):
    check_vertex_is_conform(vertex)
    check_all_coords_id(vertex)
    vertex = np.array(vertex)

    y_list = vertex[:, 1]
    mins_y = np.where(y_list == y_list.min())[0]
    if len(mins_y) == 1:
        return permutation_vertex(vertex, mins_y[0])
    else:
        x_list = vertex[mins_y, 0]
        mins_x = np.where(x_list == x_list.min())[0]
        return permutation_vertex(vertex, mins_y[mins_x[0]])
