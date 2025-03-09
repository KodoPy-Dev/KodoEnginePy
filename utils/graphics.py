from OpenGL import GL


def set_point_size(size=1.0):
    GL.glPointSize(size)


def set_depth_test(enable=False):
    if enable:
        GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glDepthFunc(GL.GL_LESS)
    else:
        GL.glDisable(GL.GL_DEPTH_TEST)


def set_blend(enable=False):
    if enable:
        GL.glEnable(GL.GL_BLEND)
        GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)
    else:
        GL.glDisable(GL.GL_BLEND)
