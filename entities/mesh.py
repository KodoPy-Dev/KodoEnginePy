from uuid import uuid4
from OpenGL import GL
import numpy as np
import glm
from ..utils import maths
from ..utils.debug import debug_print


class Mesh:
    def __init__(self, verts=[], edges=[], polys=[]):
        self.id = str(uuid4())
        self.type = 'MESH'
        self.dirty = True
        # Geometry
        self.verts = verts
        self.edges = edges
        self.polys = polys
        # Buffers
        self.vao = 0
        self.vbo = 0
        self.polys_ebo = 0
        self.edges_ebo = 0


    def rebuild_buffers(self):
        self.clear_memory()
        self.gen_buffers()
        self.cache_buffers()
        self.unbind_buffers()
        self.dirty = False


    def clear_memory(self):
        if self.vao: GL.glDeleteVertexArrays(1, [self.vao])
        if self.vbo: GL.glDeleteBuffers(1, [self.vbo])
        if self.polys_ebo: GL.glDeleteBuffers(1, [self.polys_ebo])
        if self.edges_ebo: GL.glDeleteBuffers(1, [self.edges_ebo])
        self.vao, self.vbo, self.polys_ebo, self.edges_ebo = 0, 0, 0, 0


    def gen_buffers(self):
        self.vao = GL.glGenVertexArrays(1)
        self.vbo = GL.glGenBuffers(1)
        self.polys_ebo = GL.glGenBuffers(1)
        self.edges_ebo = GL.glGenBuffers(1)


    def cache_buffers(self):
        if not self.vao or not self.vbo or not self.edges_ebo or not self.polys_ebo:
            debug_print(msg="Invalid Buffer Objects")
            return

        verts = maths.vec3_coords_to_numpy_array(self.verts)
        polys = np.fromiter((index for tri in self.polys for index in tri), dtype=np.uint32)
        edges = np.fromiter((index for edge in self.edges for index in edge), dtype=np.uint32)

        # VAO
        GL.glBindVertexArray(self.vao)
        # VBO
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.vbo)
        GL.glBufferData(GL.GL_ARRAY_BUFFER, verts.nbytes, verts, GL.GL_DYNAMIC_DRAW)
        # EBO
        GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, self.edges_ebo)
        GL.glBufferData(GL.GL_ELEMENT_ARRAY_BUFFER, edges.nbytes, edges, GL.GL_DYNAMIC_DRAW)
        # EBO
        GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, self.polys_ebo)
        GL.glBufferData(GL.GL_ELEMENT_ARRAY_BUFFER, polys.nbytes, polys, GL.GL_DYNAMIC_DRAW)
        # Attrib
        GL.glEnableVertexAttribArray(0)
        GL.glVertexAttribPointer(0, 3, GL.GL_FLOAT, GL.GL_FALSE, 12, None)


    def unbind_buffers(self):
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)
        GL.glBindVertexArray(0)


    def draw_verts(self, size=3.0):
        GL.glPointSize(size)
        GL.glBindVertexArray(self.vao)
        GL.glDrawArrays(GL.GL_POINTS, 0, len(self.verts))
        GL.glPointSize(1.0)


    def draw_edges(self, width=1.0):
        GL.glLineWidth(width)
        GL.glBindVertexArray(self.vao)
        GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, self.edges_ebo)
        GL.glDrawElements(GL.GL_LINES, len(self.edges) * 2, GL.GL_UNSIGNED_INT, None)
        GL.glLineWidth(1.0)


    def draw_polys(self):
        GL.glBindVertexArray(self.vao)
        GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, self.polys_ebo)
        GL.glDrawElements(GL.GL_TRIANGLES, len(self.polys) * 3, GL.GL_UNSIGNED_INT, None)
