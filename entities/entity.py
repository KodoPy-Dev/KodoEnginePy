from OpenGL import GL
import numpy as np
import glm
from uuid import uuid4


class Entity:
    def __init__(self, material=None, data=None):
        self.id = str(uuid4())
        self.model_mat = glm.mat4()
        self.material = material
        self.data = data


    def evaluate(self):
        if self.data is None: return
        if not self.data.dirty: return

        if self.data.type == 'MESH':
            self.data.rebuild_buffers()


    def draw_3d(self, view_mat, proj_mat):
        if self.material is None: return
        if self.data is None: return
        if self.data.dirty: return

        shader = self.material.shader
        if shader is None: return
        shader.prepare(self.model_mat, view_mat, proj_mat)

        if self.data.type == 'MESH':
            shader.set_uniform_color(self.material.poly_color)
            self.data.draw_polys()
            shader.set_uniform_color(self.material.edge_color)
            self.data.draw_edges(width=1.0)
            shader.set_uniform_color(self.material.vert_color)
            self.data.draw_verts(size=1.0)


    def clear_memory(self):
        if hasattr(self.data, 'clear_memory'):
            self.data.clear_memory()

