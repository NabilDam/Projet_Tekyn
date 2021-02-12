from shapely.geometry import Polygon
from shapely import affinity
from .order_vertex import check_coords_id
import numpy as np


def round_coords(coords):
    return round(coords[0], 5), round(coords[1], 5)


class Vertex():
    def __init__(self, vertex):
        self.vertex = vertex
        self.polygon = Polygon(vertex)

    def rotate_180(self):
        """
        Returns the self.vertex rotated of 180 degrees.

        Returns
        -------
        v_180 : tuple of tuple of float

        """
        polygon_180 = affinity.rotate(self.polygon, 180, origin='centroid')
        v_180 = tuple(polygon_180.exterior.coords)[:-1]
        v_180 = tuple(map(round_coords, v_180))
        return v_180

    def get_vertex(self):
        return self.vertex

    def translate(self, position):
        """
        Translate the self.vertex in such a way that the parameter position
         becomes equal to the first coordinates (x1, y1) of the polygone.

        Parameters
        ----------
        position : tuple of float or int

        Returns
        -------
        v_translated : tuple of tuple of float
            The polygone rotated of 180 degrees.
        """
        # Translation telle que (x1,y1) = position
        if check_coords_id(position):
            x = position[0] - self.vertex[0][0]
            y = position[1] - self.vertex[0][1]
            translation_vector = np.array((x, y))
            v_translated = self.vertex + translation_vector
            v_translated = tuple(map(round_coords, v_translated))
            return v_translated


    def __str__(self):
        return str(self.vertex)
