import glfw
import glm


class Event:
    def __init__(self):
        # Keys
        self.key = ''
        self.keys_down = set()
        # Actions
        self.action = ''
        # Modifiers
        self.shift = False
        self.ctrl = False
        self.alt = False
        # Mouse
        self.mouse_scroll = 0
        self.prev_mouse = glm.vec2(0, 0)
        self.mouse = glm.vec2(0, 0)
        # Time
        self.delta_time = 0
        self.prev_time = 0
        self.curr_time = 0


    def setup(self, app):
        # Callbacks
        window = app.window
        glfw.set_mouse_button_callback(window, self.__mouse_button_callback)
        glfw.set_scroll_callback(window, self.__scroll_callback)
        glfw.set_key_callback(window, self.__key_callback)
        # Mouse
        mouse_x, mouse_y = glfw.get_cursor_pos(window)
        self.mouse.x = mouse_x
        self.mouse.y = mouse_y
        self.prev_mouse.x = mouse_x
        self.prev_mouse.y = mouse_y
        print(self.mouse)
        print(self.prev_mouse)


    def update(self, app):
        window = app.window
        glfw.poll_events()

        # Mouse
        self.mouse_scroll = 0
        self.prev_mouse.x = self.mouse.x
        self.prev_mouse.y = self.mouse.y
        mouse_x, mouse_y = glfw.get_cursor_pos(window)
        self.mouse.x = mouse_x
        self.mouse.y = mouse_y

        # Time
        self.curr_time = glfw.get_time()
        self.delta_time = self.curr_time - self.prev_time
        self.prev_time = self.curr_time

    # ---------------- CALLBACKS ---------------- #

    def __mouse_button_callback(self, window, button, action, mods):
        pass


    def __scroll_callback(self, window, offset_x, offset_y):
        self.mouse_scroll = offset_y


    def __key_callback(self, window, key, scancode, action, mods):
        # Key
        key_name = glfw.get_key_name(key, scancode)
        self.key = key_name.title() if isinstance(key_name, str) and key_name else ''
        # Action
        if action == 0:
            self.action = 'RELEASE'
            if self.key in self.keys_down:
                self.keys_down.remove(self.key)
        elif action == 1:
            self.action = 'PRESS'
            self.keys_down.add(self.key)
        elif action == 2:
            self.action = 'REPEAT'
            self.keys_down.add(self.key)
        # Modifiers
        self.shift = mods == 1
        self.ctrl = mods == 2
        self.alt = mods == 4

