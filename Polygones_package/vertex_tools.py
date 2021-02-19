import numpy as np
from .logging_type import logging
from .order_vertex import order_polygone_id
from .Vertex import Vertex


def create_id(vertex):
    vertex = order_polygone_id(vertex)
    vertex_instance = Vertex(vertex)
    v_id = vertex_instance.translate((0, 0))
    return np.array((v_id))


def dichotomy(element, sorted_list):
    # l : une liste trié par ordre croissant
    # e : élément à trouver ou à encadrer
    # si e appartient à e alors le nombre retourné est l'indice de la liste ou ce trouve l'élément
    # si un couple est retourné alors:
    #   * couple = (0, -1) alors l'élément cherché est plus petit que le plus petit élément de la liste
    #   * couple = (-1, 1) alors l'élément cherché est plus grand que le plus grand élément de la liste
    #   * couple = (a, b) / a < b alors les éléments l[a] et l[b] encadrent l'élément cherché
    # complexity : ln2(len(l) = n))
    size = len(sorted_list)
    (a, b) = (0, size - 1)

    while b - a > 1:
        m = (a + b) // 2

        if element == sorted_list[m]:
            return m
        elif element < sorted_list[m]:
            b = m
        else:
            a = m

    if element == sorted_list[a]:
        return a
    elif element == sorted_list[b]:
        return b
    elif sorted_list[a] < element < sorted_list[b]:
        return a, b
    elif element < sorted_list[a]:
        return (0, -1)
    else:
        return (-1, 0)

    return a, b


def where_id_in_list(id_polygone, list_ids):
    index = []
    for i, id in enumerate(list_ids):
        id_polygone = set(tuple(coords) for coords in id_polygone)
        id = set(tuple(coords) for coords in id)
        if id == id_polygone:
            index.append(i)
    return index


def check_id_in_list(id_polygone, list_ids):
    id_already_exist = False
    for id in list_ids:
        id_polygone = set(tuple(coords) for coords in id_polygone)
        id = set(tuple(coords) for coords in id)
        if id == id_polygone:
            return True
    return id_already_exist


def get_id(new_polygone, new_l_ids):
    # Si jamais le polygone n'existe pas, je le retourne, je fais la même manipulation :
    # Si la version retournée existe, je récupère l'id correspondant
    # Sinon je garde le même id
    id_polygone = create_id(new_polygone)
    # Fonction à faire dans la fonction insert_final
    id_already_exist = check_id_in_list(id_polygone, new_l_ids)
    if id_already_exist:
        logging.info(f"The id of the polygone : {new_polygone} already exists")

    # On vérifie que sa rotation n'est pas déjà présente
    if not id_already_exist:
        p = Vertex(new_polygone)
        v_180 = p.rotate_180()
        v_180_id = create_id(v_180)
        if check_id_in_list(v_180_id, new_l_ids):
            id_polygone = v_180_id
            logging.info(f"The id of the polygone : {new_polygone} rotated of "
                         "180 degrees already exists")
        else:
            logging.info(f"Id created for the new polygone : {new_polygone}")

    return id_polygone


def insertion_in_lists(new_polygone, new_l_polygones, new_l_ids, index,
                       ref_position, current_list):
    id_polygone = get_id(new_polygone, new_l_ids)
    if index == (-1, 0):
        # On doit l'insérer à la fin du tableau
        new_l_polygones.insert(ref_position + len(current_list),
                               new_polygone.tolist())
        new_l_ids.insert(ref_position + len(current_list), id_polygone.tolist())
    elif index == (0, -1):
        # On doit l'insérer au début du tableau
        new_l_polygones.insert(ref_position, new_polygone.tolist())
        new_l_ids.insert(ref_position, id_polygone.tolist())
    elif type(index) == tuple:
        # Alors l'objet est entre l'indice a et b retourné
        new_l_polygones.insert(index[1] + ref_position, new_polygone.tolist())
        new_l_ids.insert(index[1] + ref_position, id_polygone.tolist())
    else:
        new_l_polygones.insert(index + ref_position, new_polygone.tolist())
        new_l_ids.insert(index + ref_position, id_polygone.tolist())

    return np.array([new_l_polygones, new_l_ids])


def find_polygone(new_polygone, array_polygones):
    nb_vertex = len(new_polygone)

    vertex_i = 0
    # On commence par les y
    xy = 1
    position_found = False
    current_array = np.copy(array_polygones)
    ref_position = 0
    while not position_found and vertex_i < nb_vertex:
        list_to_insert = current_array[:, vertex_i, xy]
        element_to_insert = new_polygone[vertex_i][xy]
        index = dichotomy(element_to_insert, list_to_insert)

        # Si yi est égal à l'élément du milieu, il faut continuer
        if type(index) != tuple:
            xy = (xy + 1) % 2
            indices = np.where(list_to_insert == element_to_insert)
            current_array = current_array[indices]
            ref_position += np.min(indices)

        else:
            position_found = True
        if xy == 1:
            vertex_i += 1

    return index, ref_position, current_array, vertex_i, position_found


def replace_vertex(vertex_translated, new_vertex):
    position = (vertex_translated[0][0], vertex_translated[0][1])
    new_vertex_translated = Vertex(new_vertex).translate(position)
    return new_vertex_translated
