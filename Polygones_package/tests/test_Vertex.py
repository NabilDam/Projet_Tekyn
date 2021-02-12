import pytest
from Polygones_package.Vertex import Vertex


@pytest.mark.rotate
def test_rotate_180():
    vertex = ((1, 2), (2, 2.5), (3, 2))
    vertex_180 = ((3.0, 2.33333), (2.0, 1.83333), (1.0, 2.33333))

    v_180 = Vertex(vertex).rotate_180()
    v_0 = Vertex(v_180).rotate_180()

    assert v_180 == vertex_180
    assert v_0 == vertex


@pytest.mark.translate
def test_translate():
    rectangle = ((1, 1), (3, 1), (3, 3), (1, 3))
    new_x1_y1 = (4, 4)

    v_translated = Vertex(rectangle).translate(new_x1_y1)

    assert v_translated[0] == new_x1_y1
