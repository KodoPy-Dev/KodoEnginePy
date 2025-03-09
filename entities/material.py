from OpenGL import GL
import numpy as np
import glm
from uuid import uuid4
from ..resources.shaders import get_shader


class Material:
    def __init__(self):
        self.id = str(uuid4())
        self.vert_color = glm.vec4(1.0, 0.0, 0.0, 1.0)
        self.edge_color = glm.vec4(0.0, 1.0, 0.0, 1.0)
        self.poly_color = glm.vec4(0.0, 0.0, 1.0, 0.25)
        self.shader = get_shader(name='UNIFORM_COLOR')


