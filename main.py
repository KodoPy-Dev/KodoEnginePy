import glfw
import glm
from OpenGL import GL
import numpy as np
from . import entities
from . import utils


SETTINGS = {
    # Window
    'WINDOW_TITLE'  : "PyEngine",
    'WINDOW_WIDTH'  : 800,
    'WINDOW_HEIGHT' : 600,
    # Graphics
    'OPENGL_VERSION'  : (4, 3),
    'OPENGL_DEBUG_ON' : True,
    'MSAA_ON'         : True,
    # Camera
    'CAM_POSITION'  : (0.0, 2.0, -5.0),
    'CAM_YAW'       : 90,
    'CAM_PITCH'     : 0.0,
    'CAM_FOV'       : 45,
    'CAM_CLIP_NEAR' : 0.01,
    'CAM_CLIP_FAR'  : 100,
    # Console
    'PRINT_SETUP_INFO' : True,
    # Event
    'CLOSE_ON_ESCAPE' : True,
    'DISABLE_CURSOR'  : True,
}


entity = None


def setup(app):
    global entity
    entity = utils.factory.gen_mesh_entity_quad(scale=5)


def update(app):
    global entity
    if entity is None:
        app.active = False
        return
    entity.evaluate()


def draw_3d(app, view_mat:glm.mat4x4, proj_mat:glm.mat4x4):
    global entity
    if entity is None:
        app.active = False
        return

    # --------------------------------------- PUT IN RENDER --------------------------------------- #
    GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
    GL.glEnable(GL.GL_LINE_SMOOTH)
    GL.glEnable(GL.GL_DEPTH_TEST)
    GL.glDepthFunc(GL.GL_LESS)
    GL.glEnable(GL.GL_BLEND)
    GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)

    entity.draw_3d(view_mat, proj_mat)

    GL.glDisable(GL.GL_DEPTH_TEST)
    GL.glDisable(GL.GL_BLEND)


def draw_2d(app, viewport_width:int, viewport_height:int):
    pass


def close():
    global entity
    if entity is not None:
        entity.clear_memory()
