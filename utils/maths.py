import math
import glm
import numpy as np


def vec2_coords_to_numpy_array(coords):
    return np.fromiter((comp for coord in coords for comp in (coord.x, coord.y)), dtype=np.float32)


def vec3_coords_to_numpy_array(coords):
    return np.fromiter((comp for coord in coords for comp in (coord.x, coord.y, coord.z)), dtype=np.float32)


def numpy_array_to_vec2_coords(array):
    return [glm.vec2(*row) for row in array.reshape(-1, 2)]


def numpy_array_to_vec3_coords(array):
    return [glm.vec3(*row) for row in array.reshape(-1, 3)]


def vec2_coords_ss_to_vec2_coords_ndc(coords, viewport_width:int, viewport_height:int):
    inv_w = 2.0 / viewport_width
    inv_h = 2.0 / viewport_height
    return [glm.vec2((coord.x * inv_w) - 1.0, 1.0 - (coord.y * inv_h)) for coord in coords]
