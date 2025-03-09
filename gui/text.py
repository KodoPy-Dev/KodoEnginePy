from pathlib import Path
import glfw
import numpy as np
import freetype
from OpenGL.GL import *
import glm

# Initialize GLFW
if not glfw.init():
    raise Exception("Failed to initialize GLFW")

window = glfw.create_window(800, 600, "OpenGL Text Rendering", None, None)
glfw.make_context_current(window)

# Load FreeType and prepare character textures

from ..resources.fonts import get_font_file
font_file = get_font_file(file_name="Roboto-Regular", extension="tff")
face = freetype.Face(font_file)
face.set_pixel_sizes(0, 48)
characters = {}

for char in range(128):
    face.load_char(chr(char), freetype.FT_LOAD_RENDER)
    bitmap = face.glyph.bitmap
    tex_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, tex_id)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RED, bitmap.width, bitmap.rows, 0, GL_RED, GL_UNSIGNED_BYTE, bitmap.buffer)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    characters[chr(char)] = {'texture': tex_id, 'size': glm.vec2(bitmap.width, bitmap.rows),
                             'bearing': glm.vec2(face.glyph.bitmap_left, face.glyph.bitmap_top),
                             'advance': face.glyph.advance.x}

vao = glGenVertexArrays(1)
vbo = glGenBuffers(1)
glBindVertexArray(vao)
glBindBuffer(GL_ARRAY_BUFFER, vbo)
glBufferData(GL_ARRAY_BUFFER, 6 * 4 * 4, None, GL_DYNAMIC_DRAW)
glEnableVertexAttribArray(0)
glVertexAttribPointer(0, 4, GL_FLOAT, GL_FALSE, 4 * 4, ctypes.c_void_p(0))
glBindBuffer(GL_ARRAY_BUFFER, 0)
glBindVertexArray(0)

vertex_shader = """
#version 330 core
layout (location = 0) in vec4 vertex;
out vec2 TexCoords;
uniform mat4 projection;
void main() {
    gl_Position = projection * vec4(vertex.xy, 0.0, 1.0);
    TexCoords = vertex.zw;
}
"""

fragment_shader = """
#version 330 core
in vec2 TexCoords;
out vec4 color;
uniform sampler2D text;
uniform vec3 textColor;
void main() {
    float alpha = texture(text, TexCoords).r;
    color = vec4(textColor, alpha);
}
"""

def compile_shader(source, shader_type):
    shader = glCreateShader(shader_type)
    glShaderSource(shader, source)
    glCompileShader(shader)
    if glGetShaderiv(shader, GL_COMPILE_STATUS) != GL_TRUE:
        raise RuntimeError(glGetShaderInfoLog(shader))
    return shader

shader_program = glCreateProgram()
vs = compile_shader(vertex_shader, GL_VERTEX_SHADER)
fs = compile_shader(fragment_shader, GL_FRAGMENT_SHADER)
glAttachShader(shader_program, vs)
glAttachShader(shader_program, fs)
glLinkProgram(shader_program)
glUseProgram(shader_program)
projection = glm.ortho(0.0, 800.0, 0.0, 600.0)
glUniformMatrix4fv(glGetUniformLocation(shader_program, "projection"), 1, GL_FALSE, glm.value_ptr(projection))

def render_text(text, x, y, scale, color):
    glUseProgram(shader_program)
    glUniform3f(glGetUniformLocation(shader_program, "textColor"), *color)
    glActiveTexture(GL_TEXTURE0)
    glBindVertexArray(vao)
    for char in text:
        if char in characters:
            ch = characters[char]
            xpos = x + ch['bearing'].x * scale
            ypos = y - (ch['size'].y - ch['bearing'].y) * scale
            w = ch['size'].x * scale
            h = ch['size'].y * scale
            vertices = np.array([
                xpos, ypos + h, 0.0, 0.0,
                xpos, ypos, 0.0, 1.0,
                xpos + w, ypos, 1.0, 1.0,
                xpos, ypos + h, 0.0, 0.0,
                xpos + w, ypos, 1.0, 1.0,
                xpos + w, ypos + h, 1.0, 0.0,
            ], dtype=np.float32)
            glBindTexture(GL_TEXTURE_2D, ch['texture'])
            glBindBuffer(GL_ARRAY_BUFFER, vbo)
            glBufferSubData(GL_ARRAY_BUFFER, 0, vertices.nbytes, vertices)
            glDrawArrays(GL_TRIANGLES, 0, 6)
            x += (ch['advance'] >> 6) * scale
    glBindVertexArray(0)
    glBindTexture(GL_TEXTURE_2D, 0)

while not glfw.window_should_close(window):
    glClear(GL_COLOR_BUFFER_BIT)
    render_text("Hello OpenGL!", 50, 500, 1.0, (1.0, 1.0, 1.0))
    glfw.swap_buffers(window)
    glfw.poll_events()

glfw.terminate()
