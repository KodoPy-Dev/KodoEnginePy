import numpy as np
import glm


def gen_mesh_entity_triangle():
    from ..entities import Entity, Material, Mesh

    material = Material()

    p1 = glm.vec3(-0.5, -0.5, 0.0)
    p2 = glm.vec3( 0.5, -0.5, 0.0)
    p3 = glm.vec3( 0.0,  0.5, 0.0)
    verts = [p1, p2, p3]
    edges = [(0, 1), (1, 2), (2, 0)]
    polys = [(0, 1, 2)]
    mesh = Mesh(verts=verts, edges=edges, polys=polys)

    entity = Entity(material=material, data=mesh)
    return entity


def gen_mesh_entity_quad(scale=5):
    from ..entities import Entity, Material, Mesh

    material = Material()

    p1 = glm.vec3(-scale, 0.0, -scale) # BL
    p2 = glm.vec3(-scale, 0.0,  scale) # TL
    p3 = glm.vec3( scale, 0.0,  scale) # TR
    p4 = glm.vec3( scale, 0.0, -scale) # BR
    verts = [p1, p2, p3, p4]
    edges = [(0, 1), (1, 2), (2, 3), (3, 0)]
    polys = [(0, 1, 2), (0, 2, 3)]
    mesh = Mesh(verts=verts, edges=edges, polys=polys)

    entity = Entity(material=material, data=mesh)
    return entity


def gen_mesh_entity_cube():
    pass


def gen_mesh_entity_uv_sphere():
    pass


def gen_mesh_entity_ico_sphere():
    pass


