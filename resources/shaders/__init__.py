from OpenGL import GL
import numpy as np
import glm
from pathlib import Path


SHADERS = {
    'UNIFORM_COLOR' : None,
}


def create_shaders():
    global SHADERS
    # Uniform Color
    shader = Shader_UniformColor()
    if shader.create():
        SHADERS['UNIFORM_COLOR'] = shader


def get_shader(name=''):
    global SHADERS
    if name in SHADERS:
        return SHADERS[name]
    return None


def delete_shaders():
    global SHADERS
    for shader in SHADERS.values():
        shader.close()
    for key in SHADERS.keys():
        SHADERS[key] = None


def get_shader_source(file_name="", extension="glsl"):
    shaders_dir = Path(__file__).parent.resolve()
    shader_file = shaders_dir.joinpath(f"{file_name}.{extension}")
    if shader_file.exists():
        with open(shader_file, 'r', encoding='utf-8') as file:
            return file.read()
    return ""


def compile_shader_source(shader_type, source):
    # Shader | Source | Compile
    shader = GL.glCreateShader(shader_type)
    GL.glShaderSource(shader, source)
    GL.glCompileShader(shader)
    # Error
    if GL.glGetShaderiv(shader, GL.GL_COMPILE_STATUS) != GL.GL_TRUE:
        error_log = GL.glGetShaderInfoLog(shader).decode()
        GL.glDeleteShader(shader)
        print(f"Shader compilation failed:\n{error_log}")
        return None
    return shader


class Shader_UniformColor:
    def __init__(self):
        self.program = None
        # Uniforms
        self.UL_model = None
        self.UL_view  = None
        self.UL_proj  = None
        self.UL_color = None


    def create(self):
        # Free
        self.close()
        # Source
        vert_source = get_shader_source(file_name="uniform_color_vert", extension="glsl")
        frag_source = get_shader_source(file_name="uniform_color_frag", extension="glsl")
        # Error
        if not vert_source or not frag_source:
            return False
        # Shaders
        vertex_shader = compile_shader_source(shader_type=GL.GL_VERTEX_SHADER, source=vert_source)
        fragment_shader = compile_shader_source(shader_type=GL.GL_FRAGMENT_SHADER, source=frag_source)
        # Error
        if vertex_shader is None or fragment_shader is None:
            if vertex_shader is not None:
                GL.glDeleteShader(vertex_shader)
            if fragment_shader is not None:
                GL.glDeleteShader(fragment_shader)
            return False
        # Program
        self.program = GL.glCreateProgram()
        GL.glAttachShader(self.program, vertex_shader)
        GL.glAttachShader(self.program, fragment_shader)
        GL.glLinkProgram(self.program)
        # Free
        GL.glDeleteShader(vertex_shader)
        GL.glDeleteShader(fragment_shader)
        # Error
        if GL.glGetProgramiv(self.program, GL.GL_LINK_STATUS) != GL.GL_TRUE:
            error_log = GL.glGetProgramInfoLog(self.program).decode()
            print(f"Shader program linking failed:\n{error_log}")
            self.close()
            return False
        # Uniforms
        self.UL_model = GL.glGetUniformLocation(self.program, "model")
        self.UL_view  = GL.glGetUniformLocation(self.program, "view")
        self.UL_proj  = GL.glGetUniformLocation(self.program, "projection")
        self.UL_color = GL.glGetUniformLocation(self.program, "color")
        # Valid
        return True


    def prepare(self, model_mat, view_mat, proj_mat):
        if self.program is None: return
        GL.glUseProgram(self.program)
        GL.glUniformMatrix4fv(self.UL_model, 1, GL.GL_FALSE, glm.value_ptr(model_mat))
        GL.glUniformMatrix4fv(self.UL_view , 1, GL.GL_FALSE, glm.value_ptr(view_mat))
        GL.glUniformMatrix4fv(self.UL_proj , 1, GL.GL_FALSE, glm.value_ptr(proj_mat))


    def set_uniform_color(self, color):
        GL.glUniform4fv(self.UL_color, 1, glm.value_ptr(color))


    def close(self):
        if self.program is not None:
            GL.glDeleteProgram(self.program)
        self.program = None
