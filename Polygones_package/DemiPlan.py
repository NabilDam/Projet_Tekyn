from .logging_type import logging
from .vertex_tools import insertion_in_lists, create_id, \
    find_polygone, where_id_in_list, replace_vertex
from .order_vertex import order_polygone, check_coords_id
from Polygones_package import Vertex
import numpy as np
from shapely.geometry import Polygon
import matplotlib.pyplot as plt
import geopandas as gpd


def warning_already_exists():
    logging.warning("Warning : The polygone is already in the collection")


class DemiPlan():
    def __init__(self):
        self.collection = dict()

    def get_both_lists(self, new_polygone):
        nb_vertex = len(new_polygone)
        if not nb_vertex in self.collection:
            self.collection[nb_vertex] = [[], []]
        both_lists = self.collection[nb_vertex]
        return both_lists[0], both_lists[1]

    def insert_polygone(self, new_polygone):
        """
        Insert the polygone in the sorted collection.

        Parameters
        ----------
        new_polygone : array or tuple of tuple of float

        Returns
        -------

        """
        new_polygone = order_polygone(new_polygone)
        nb_vertex = len(new_polygone)
        array_polygones, array_ids = self.get_both_lists(new_polygone)
        if len(array_polygones) == 0:
            self.collection[nb_vertex][0] = np.array([new_polygone])
            self.collection[nb_vertex][1] = np.array(
                [create_id(new_polygone)])
            return

        index, ref_position, current_array, vertice_i, position_found = \
            find_polygone(new_polygone, array_polygones)

        if (vertice_i == nb_vertex) and not (position_found):
            logging.info(f"The polygone : {new_polygone}"
                         f" already exists in this position")
            return np.array([array_polygones, array_ids])

        new_l_polygones = array_polygones.tolist()
        new_l_ids = array_ids.tolist()
        polygones, ids = insertion_in_lists(new_polygone, new_l_polygones,
                                            new_l_ids, index, ref_position,
                                            current_array)
        self.collection[nb_vertex][0] = polygones
        self.collection[nb_vertex][1] = ids

    def replace(self, polygone_to_replace, new_polygone):
        """
        Replace the "polygone_to_replace" in the collection by the
        "new_polygone" at all positions where the "polygone_to_replace" was.

        Parameters
        ----------
        polygone_to_replace : array or tuple of tuple of float
        new_vertex : array or tuple of tuple of float

        Returns
        -------

        """
        # Parcourir une seule fois toute la collection[nb_vertex][1] (les ids)
        # A chaque fois qu'on trouve l'id en question, on remplace le polygone.
        # ATTENTION Il y a un calcule de translation à faire
        # pour créer la bonne position à chaque fois.
        new_polygone = order_polygone(new_polygone)
        polygone_to_replace = order_polygone(polygone_to_replace)
        nb_vertex = len(polygone_to_replace)
        id_polygone = create_id(polygone_to_replace)
        array_polygones, array_ids = self.get_both_lists(polygone_to_replace)
        list_ids = array_ids.tolist()
        index = where_id_in_list(id_polygone, list_ids)

        if len(index) == 0:
            logging.info("The polygone to "
                         " doesn't exist in the collection")
            return

        # On récupère l'id du poylgone
        new_vertex_id = create_id(new_polygone)
        for i in index:
            vertex_translated = self.collection[nb_vertex][0][i]
            new_vertex_translated = replace_vertex(
                vertex_translated, new_polygone)
            self.collection[nb_vertex][0][i] = new_vertex_translated
            self.collection[nb_vertex][1][i] = new_vertex_id

    def delete_polygone(self, polygone):
        """
        Delete the exact same polygone passed in parameter
         and not at all his positions.

        Parameters
        ----------
        polygone : array or tuple of tuple of float

        Returns
        -------

        """
        polygone = order_polygone(polygone)
        nb_vertex = len(polygone)
        array_polygones, array_ids = self.get_both_lists(polygone)
        if len(array_polygones) == 0:
            logging.info(f"The polygone : {polygone}"
                         f" doesn't exist in the collection")
            return

        index, ref_position, current_array, vertice_i, position_found = \
            find_polygone(polygone, array_polygones)

        if (vertice_i != nb_vertex) or (position_found):
            logging.info(f"The polygone : {polygone}"
                         f" doesn't exist in the collection")
            return np.array([array_polygones, array_ids])

        self.collection[nb_vertex][0] = np.delete(
            self.collection[nb_vertex][0], ref_position, axis=0)
        self.collection[nb_vertex][1] = np.delete(
            self.collection[nb_vertex][1], ref_position, axis=0)

    def delete_entirely(self, polygone):
        """
        Delete all the polygones in the collection having the same id
        than the one passed in parameter.
        It will delete the polygone at all his positions.

        Parameters
        ----------
        polygone : array or tuple of tuple of float

        Returns
        -------

        """
        # Va supprimer le polygone à toutes ses positions
        polygone = order_polygone(polygone)
        nb_vertex = len(polygone)
        id_polygone = create_id(polygone)
        array_polygones, array_ids = self.get_both_lists(polygone)
        list_ids = array_ids.tolist()
        index = where_id_in_list(id_polygone, list_ids)

        if len(index) == 0:
            logging.info("The polygone doesn't exist in the collection")
            return
        self.collection[nb_vertex][0] = np.delete(
            self.collection[nb_vertex][0], index, axis=0)
        self.collection[nb_vertex][1] = np.delete(
            self.collection[nb_vertex][1], index, axis=0)

        if len(self.collection[nb_vertex][0]) == 0:
            del self.collection[nb_vertex]

    def pop_lowest_polygone(self):
        """
        Delete the polygone with the lowest y-axis in the collection
        and returns it.

        Returns
        -------
        lowest_polygone : array of tuple of float

        """
        # Chercher le type de polygone ayant l'ordonnée la plus petite :
        if len(self.collection) == 0:
            logging.info("There is no polygone in the collection")
            return
        polygone_min = list(self.collection)[0]
        # 1er [0] : pour la liste de polygones
        # 2eme [0] : Pour le plus bas poylgone dans la liste
        # 3eme [0] : Pour obtenir sa premiere coordonnée
        # [1] : Pour obtenir le y le plus petit
        min_y = self.collection[polygone_min][0][0][0][1]
        for vertex in self.collection:
            current_y = self.collection[vertex][0][0][0][1]
            if current_y < min_y:
                min_y = current_y
                polygone_min = vertex
        lowest_polygone = self.collection[polygone_min][0][0]
        self.collection[polygone_min][0] = np.delete(
            self.collection[polygone_min][0], 0, axis=0)
        self.collection[polygone_min][1] = np.delete(
            self.collection[polygone_min][1], 0, axis=0)
        return lowest_polygone

    def retrieve_polygone(self, polygone):
        """
        Retrieve all polygones in the collection having the same id
         than the one passed in parameters.
        Returns all polygones found and there positions.
        A position is defined by the first coordinates of the polygone (x1, y1)

        Parameters
        ----------
        polygone : array or tuple of tuple of float

        Returns
        -------
        polygones : list of polygones
        positions : list of tuple

        """
        # Retrouve tous polygones du même type et
        # récupère également les positions des (x1, y1)
        polygone = order_polygone(polygone)
        nb_vertex = len(polygone)
        id_polygone = create_id(polygone)
        array_polygones, array_ids = self.get_both_lists(polygone)
        list_ids = array_ids.tolist()
        index = where_id_in_list(id_polygone, list_ids)

        if len(index) == 0:
            logging.info("The polygone doesn't exist in the collection")
            return
        polygones = self.collection[nb_vertex][0][index]
        positions = polygones[:, 0]
        return polygones, positions

    def move_polygone(self, polygone, new_position):
        """
        Find the exact same polygone in the collection and translate
        it so the (x1, y1) becomes equal to "new_position".
        Deletes the polygone in the old position
        and inserts the polygone in the new postion.

        Parameters
        ----------
        polygone : list of polygones
        new_position : list of tuple

        Returns
        -------

        """
        self.delete_polygone(polygone)
        polygone_translated = Vertex(polygone).translate(new_position)
        self.insert_polygone(polygone_translated)

    def get_polygones_between(self, y_min, y_max):
        """

        Parameters
        ----------
        y_min : int or float
            The polygones in the list returned have to be upper than y_min
        y_max : int or float
            The polygones in the list returned have to be under y_max
        Returns
        -------
        polygones_between : list of polygones

        """
        check_coords_id((y_min, y_max))
        polygones_between = dict()
        for nb_vertex in self.collection:
            array_polygones = self.collection[nb_vertex][0]
            for polygone in array_polygones:
                y_i_min = polygone[0][1]
                y_i_max = np.max(polygone[:, 1])
                if y_i_min >= y_max:
                    break
                if y_i_min >= y_min and y_i_max <= y_max:
                    if nb_vertex not in polygones_between:
                        polygones_between[nb_vertex] = []
                    polygones_between[nb_vertex].append(polygone)
        return polygones_between

    def visualize_polygones(self, file_path):
        """
        Creates a graph showing all polygones in the collection.
        There is only one color, so if some polygones are superimposed, it's
        not possible to distinguish them.

        Parameters
        ----------
        file_path : str
            The path name of the file created to visualize polygones.
        Returns
        -------

        """
        # Attention tous les polygones ont la même couleur
        # s'ils sont superposés, on ne les verra pas
        if type(file_path) != str:
            logging.error("The namefile must be a string")
            raise
        polygones = self.get_all_polygones()
        if len(polygones) == 0:
            logging.info("There is no polygone in the collection")
            return
        polygones_instances = []
        for polygone in polygones:
            polygones_instances.append(Polygon(polygone))
        p = gpd.GeoSeries(polygones_instances)
        p.plot()
        plt.savefig(file_path)

    def get_all_polygones(self):
        res = []
        if len(self.collection) == 0:
            return []
        for nb_vertex in self.collection:
            res.extend(self.collection[nb_vertex][0])
        return res

    def get_collection(self):
        return self.collection

    def __str__(self):
        return str(self.collection)
