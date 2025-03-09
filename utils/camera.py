import glm
import glfw
import math
from math import cos, sin, radians


class Camera:
    def __init__(self):
        # Settings
        self.move_speed = 2.5
        self.mouse_sensitivity = 5.0
        # Motion
        self.position = glm.vec3(0,0,0)
        self.world_up = glm.vec3(0,1,0)
        self.yaw = 0
        self.pitch = 0
        self.front = glm.vec3(0.0, 0.0, 1.0)
        self.right = glm.vec3(1.0, 0.0, 0.0)
        self.up = glm.vec3(0.0, 1.0, 0.0)
        # Projections
        self.fov = 45
        self.clip_near = 0.1
        self.clip_far = 500
        self.view_mat = glm.mat4x4()
        self.proj_mat_2d = glm.mat4x4()
        self.proj_mat_3d = glm.mat4x4()


    def setup(self, app, position=(0.0, 0.0, 0.0), yaw=0.0, pitch=0.0, fov=45, clip_near=0.1, clip_far=100):
        self.position = glm.vec3(position)
        self.yaw = yaw
        self.pitch = pitch
        self.fov = fov
        self.clip_near = clip_near
        self.clip_far = clip_far
        self.set_view_matrix()
        self.set_projection_matrices(width=app.width, height=app.height)


    def update(self, app):
        # Event
        event = app.event
        delta_time = event.delta_time
        delta = self.move_speed * delta_time

        # Mod Speed
        if event.shift:
            delta *= 2
        elif event.ctrl:
            delta /= 2

        # Position Offset
        offset = glm.vec3(0,0,0)

        # Keyboard
        if 'W' in event.keys_down:
            offset += self.front
        if 'S' in event.keys_down:
            offset -= self.front
        if 'A' in event.keys_down:
            offset -= self.right
        if 'D' in event.keys_down:
            offset += self.right
        if 'Q' in event.keys_down:
            offset -= self.up
        if 'E' in event.keys_down:
            offset += self.up

        # Scroll
        if event.mouse_scroll == 1:
            offset += self.front
        elif event.mouse_scroll == -1:
            offset -= self.front

        # Position
        if glm.length(offset) > 0:
            self.position += glm.normalize(offset) * delta

        # Mouse
        offset_x = (event.mouse.x - event.prev_mouse.x) * self.mouse_sensitivity * delta_time
        offset_y = (event.mouse.y - event.prev_mouse.y) * self.mouse_sensitivity * delta_time
        self.yaw += offset_x
        self.pitch -= offset_y
        self.pitch = max(-89.0, min(89.0, self.pitch))

        # View
        self.set_view_matrix()

    # ---------------- SETTERS ---------------- #

    def set_view_matrix(self):
        front = glm.vec3()
        front.x = cos(radians(self.yaw)) * cos(radians(self.pitch))
        front.y = sin(radians(self.pitch))
        front.z = sin(radians(self.yaw)) * cos(radians(self.pitch))
        self.front = glm.normalize(front)
        self.right = glm.normalize(glm.cross(self.front, self.world_up))
        self.up = glm.normalize(glm.cross(self.right, self.front))
        self.view_mat = glm.lookAt(self.position, self.position + self.front, self.up)


    def set_projection_matrices(self, width, height):
        aspect_ratio = width / height
        self.proj_mat_2d = glm.ortho(0, width, height, 0, -1, 1)
        self.proj_mat_3d = glm.perspective(self.fov, aspect_ratio, self.clip_near, self.clip_far)

