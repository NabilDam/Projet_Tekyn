import pytest
from Polygones_package.DemiPlan import DemiPlan
from Polygones_package.Vertex import Vertex
import numpy as np


def check_lists_equals(list_v1, list_v2):
    for vertex_1, vertex_2 in zip(list_v1, list_v2):
        for coords_1, coords_2 in zip(vertex_1, vertex_2):
            if tuple(coords_1) != tuple(coords_2):
                return False
    return True


def check_collection_equals(col_1, col_2):
    for key_1 in col_1:
        polygones_1, ids_1 = col_1[key_1][0], col_1[key_1][1]
        polygones_2, ids_2 = col_2[key_1][0], col_2[key_1][1]
        c1 = check_lists_equals(polygones_1, polygones_2)
        c2 = check_lists_equals(ids_1, ids_2)
        if (c1 and c2) == False:
            return False
    return True


@pytest.mark.insert
def test_insert_polygone():
    plan = DemiPlan()

    T1 = np.array(((1, 2), (2, 2.5), (3, 2)))

    col1 = {3: [np.array([[[1., 2.],
                           [2., 2.5],
                           [3., 2.]]]), np.array([[[0., 0.],
                                                   [1., 0.5],
                                                   [2., 0.]]])]}

    plan.insert_polygone(T1)
    # Vérifions que T1 a bien été ajouté à la collection :
    assert check_collection_equals(col1, plan.get_collection()) is True

    # Vérifions que T1 n'a pas été ajouté deux fois :
    plan.insert_polygone(T1)
    assert check_collection_equals(col1, plan.get_collection()) is True

    # Vérifions que T2 a été ajouté dans l'ordre (après T1)
    T2 = np.array(((1, 9.52), (2, 3), (3.94, 2)))
    plan.insert_polygone(T2)

    col2 = {3: [np.array([[[1., 2.],
                           [2., 2.5],
                           [3., 2.]],

                          [[3.94, 2.],
                           [1., 9.52],
                           [2., 3.]]]), np.array([[[0., 0.],
                                                   [1., 0.5],
                                                   [2., 0.]],

                                                  [[0., 0.],
                                                   [-2.94, 7.52],
                                                   [-1.94, 1.]]])]}

    assert check_collection_equals(col2, plan.get_collection()) is True

    plan = DemiPlan()
    plan.insert_polygone(T1)
    # Vérifions qu'il n'y a pas de deuxième id créé pour la version à 180 degrés
    T1_180 = Vertex(T1).rotate_180()
    plan.insert_polygone(T1_180)
    col3 = {3: [np.array([[[2., 1.83333],
                           [1., 2.33333],
                           [3., 2.33333]],

                          [[1., 2.],
                           [2., 2.5],
                           [3., 2.]]]), np.array([[[0., 0.],
                                                   [1., 0.5],
                                                   [2., 0.]],

                                                  [[0., 0.],
                                                   [1., 0.5],
                                                   [2., 0.]]])]}

    assert check_collection_equals(col3, plan.get_collection()) is True
    # Vérifions que une double rotation à 180 revient au polygone de départ.
    plan.insert_polygone(Vertex(T1_180).rotate_180())
    assert check_collection_equals(col3, plan.get_collection()) is True

    # Vérifions qu'il est possible de positionner le même polygone
    # à un endroit différent (à une translation près)
    plan = DemiPlan()
    plan.insert_polygone(T1)
    plan.insert_polygone(Vertex(T1).translate((4, 5)))
    col4 = {3: [np.array([[[1., 2.],
                           [2., 2.5],
                           [3., 2.]],

                          [[4., 5.],
                           [5., 5.5],
                           [6., 5.]]]), np.array([[[0., 0.],
                                                   [1., 0.5],
                                                   [2., 0.]],

                                                  [[0., 0.],
                                                   [1., 0.5],
                                                   [2., 0.]]])]}

    assert check_collection_equals(col4, plan.get_collection()) is True


@pytest.mark.replace
def test_replace():
    plan = DemiPlan()
    T1 = np.array(((1, 2), (2, 2.5), (3, 2)))
    T1_translated = Vertex(T1).translate((5, 5))
    T3 = np.array(((1, 2), (2, 2.5), (9, 9)))
    plan.insert_polygone(T1)
    plan.insert_polygone(T1_translated)
    plan.replace(T1, T3)
    col = {3: [np.array([[[1., 2.],
                          [2., 2.5],
                          [9., 9.]],

                         [[5., 5.],
                          [6., 5.5],
                          [13., 12.]]]), np.array([[[0., 0.],
                                                    [1., 0.5],
                                                    [8., 7.]],

                                                   [[0., 0.],
                                                    [1., 0.5],
                                                    [8., 7.]]])]}
    assert check_collection_equals(col, plan.get_collection()) is True


@pytest.mark.delete
def test_delete_polygone():
    plan = DemiPlan()
    T1 = np.array(((1, 2), (2, 2.5), (3, 2)))
    T1_translated = Vertex(T1).translate((5, 5))
    plan.insert_polygone(T1)
    plan.insert_polygone(T1_translated)
    plan.delete_polygone(T1)
    col = {3: [np.array([[[5., 5.],
                          [6., 5.5],
                          [7., 5.]]]), np.array([[[0., 0.],
                                                  [1., 0.5],
                                                  [2., 0.]]])]}
    assert check_collection_equals(col, plan.get_collection()) is True


@pytest.mark.delete
def test_delete_entirely():
    plan = DemiPlan()
    T1 = np.array(((1, 2), (2, 2.5), (3, 2)))
    T1_translated = Vertex(T1).translate((5, 5))
    plan.insert_polygone(T1)
    plan.insert_polygone(T1_translated)
    plan.delete_entirely(T1)
    col = {}
    assert check_collection_equals(col, plan.get_collection()) is True


@pytest.mark.lowest
def test_pop_lowest_polygone():
    plan = DemiPlan()
    T1 = np.array(((1, 1), (1, 2), (1, 3)))
    T2 = np.array(((1, 4), (2, 5), (3, 6)))
    plan.insert_polygone(T1)
    plan.insert_polygone(T2)
    lowest_polygone = plan.pop_lowest_polygone()
    assert check_lists_equals([lowest_polygone], [T1]) is True


@pytest.mark.retrieve
def test_retrieve_polygone():
    plan = DemiPlan()
    T1 = np.array(((1, 1), (1, 2), (1, 3)))
    T2 = np.array(((1, 4), (2, 5), (3, 6)))
    plan.insert_polygone(T1)
    plan.insert_polygone(T2)
    t2_bis, positions = plan.retrieve_polygone(T2)
    t2_bis = t2_bis[0]
    positions = tuple(positions[0])
    assert check_lists_equals([t2_bis], [T2]) is True
    assert positions == (1, 4)

@pytest.mark.move
def test_move_polygone():
    plan = DemiPlan()
    T1 = np.array(((1, 1), (1, 2), (1, 3)))
    plan.insert_polygone(T1)
    plan.move_polygone(T1, (6, 6))

    plan2 = DemiPlan()
    plan2.insert_polygone(Vertex(T1).translate((6, 6)))
    assert check_collection_equals(plan2.get_collection(),
                                   plan.get_collection()) is True


@pytest.mark.between
def test_get_polygones_between():
    plan = DemiPlan()
    T1 = np.array(((1, 1), (1, 2), (1, 3)))
    T2 = np.array(((1, 5), (1, 6), (1, 7)))
    T3 = np.array(((1, 5.5), (1, 6), (1, 6.5)))
    plan.insert_polygone(T1)
    plan.insert_polygone(T2)
    plan.insert_polygone(T3)
    res = plan.get_polygones_between(5, 7)
    assert check_lists_equals([T2, T3], res[3]) is True
