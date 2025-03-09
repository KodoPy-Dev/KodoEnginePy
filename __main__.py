import traceback
import glfw
import glm
from OpenGL import GL
from . import main
from .utils.camera import Camera
from .utils.event import Event


class App:
    def __init__(self):
        # Flags
        self.active = False
        # Window
        self.width = 800
        self.height = 600
        self.title = "App"
        self.window = None
        # Event
        self.close_on_escape = False
        # Components
        self.event = Event()
        self.camera = Camera()


    def setup(self):
        # Initializer Settings
        settings = main.SETTINGS
        self.width = settings['WINDOW_WIDTH']
        self.height = settings['WINDOW_HEIGHT']
        self.title = settings['WINDOW_TITLE']
        self.close_on_escape = settings['CLOSE_ON_ESCAPE']

        # Initialize GLFW
        glfw_initialized = glfw.init()
        if not glfw_initialized:
            print("Failed to initialize GLFW")
            return

        # Error Callback
        glfw.set_error_callback(self.__error_callback)

        # Window Hints
        version = settings['OPENGL_VERSION']
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, version[0])
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, version[1])
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL.GL_TRUE)
        if settings['OPENGL_DEBUG_ON']:
            glfw.window_hint(glfw.OPENGL_DEBUG_CONTEXT, glfw.TRUE)
        if settings['MSAA_ON']:
            glfw.window_hint(glfw.SAMPLES, 4)

        # Create window
        self.window = glfw.create_window(self.width, self.height, self.title, None, None)
        if not self.window:
            glfw.terminate()
            self.window = None
            print("Failed to create GLFW window")
            return

        # OpenGl Context
        glfw.make_context_current(self.window)

        # Resize
        glfw.set_window_size_callback(self.window, self.__window_resize_callback)

        # Lock Cursor
        if settings['DISABLE_CURSOR']:
            if glfw.raw_mouse_motion_supported():
                glfw.set_input_mode(self.window, glfw.CURSOR, glfw.CURSOR_DISABLED)
                glfw.set_input_mode(self.window, glfw.RAW_MOUSE_MOTION, True)
                self.center_cursor()

        # Event
        self.event.setup(app=self)

        # Camera
        self.camera.setup(
            app=self,
            position=settings['CAM_POSITION'],
            yaw=settings['CAM_YAW'],
            pitch=settings['CAM_PITCH'],
            fov=settings['CAM_FOV'],
            clip_near=settings['CAM_CLIP_NEAR'],
            clip_far=settings['CAM_CLIP_FAR'])

        # Print Info
        if settings['PRINT_SETUP_INFO']:
            print(f"GLFW VERSION : {glfw.get_version_string()}")
            print(f"OPENGL VERSION : {GL.glGetString(GL.GL_VERSION)}")
            print(f"OPENGL RENDERER : {GL.glGetString(GL.GL_RENDERER)}")
            print(f"OPENGL GLSL VERSION : {GL.glGetString(GL.GL_SHADING_LANGUAGE_VERSION)}")
            print("Setup Complete\n")

        # Setup Completed (main.setup can turn this off)
        self.active = True
        
        # Shaders
        from .resources.shaders import create_shaders
        create_shaders()

        # Main
        try: main.setup(app=self)
        except Exception as e:
            print("Main Setup Failed\n")
            traceback.print_exc()
            self.active = False


    def run(self):
        # Application Loop
        while self.active:

            # Active State
            self.active = not glfw.window_should_close(self.window)
            if self.close_on_escape:
                if glfw.get_key(self.window, glfw.KEY_ESCAPE) == glfw.PRESS:
                    self.active = False
                    return
            if not self.active:
                return

            # Camera
            self.camera.update(app=self)
            view_mat = self.camera.view_mat
            proj_mat_2d = self.camera.proj_mat_2d
            proj_mat_3d = self.camera.proj_mat_3d

            # Main Update
            try: main.update(app=self)
            except Exception as e:
                print("Error : App Main Update\n")
                traceback.print_exc()
                self.active = False
                return

            # Main Draw 3D
            try: main.draw_3d(app=self, view_mat=view_mat, proj_mat=proj_mat_3d)
            except Exception as e:
                print("Error : App Main Draw 3D\n")
                traceback.print_exc()
                self.active = False
                return

            # Main Draw 2D
            try: main.draw_2d(app=self, viewport_width=self.width, viewport_height=self.height)
            except Exception as e:
                print("Error : App Main Draw 2D\n")
                traceback.print_exc()
                self.active = False
                return

            # Event
            self.event.update(app=self)

            # Buffer
            glfw.swap_buffers(self.window)


    def close(self):
        self.active = False
        # Main
        try: main.close()
        except Exception as e:
            print("Error : App Main Close\n")
            traceback.print_exc()
        # Shaders
        from .resources.shaders import delete_shaders
        delete_shaders()
        # Window
        if self.window:
            try: glfw.set_window_should_close(self.window, True)
            except: pass
        # Free GLFW
        glfw.terminate()

    # ---------------- PUBLIC UTILS ---------------- #

    def center_cursor(self):
        width, height = glfw.get_window_size(self.window)
        center_x, center_y = width / 2, height / 2
        glfw.set_cursor_pos(self.window, center_x, center_y)

    # ---------------- CALLBACKS ---------------- #

    def __error_callback(self, error, description):
        print(f"GLFW Error ({error}): {description}\n")
        self.active = False


    def __window_resize_callback(self, window, width, height):
        self.width = width
        self.height = height
        self.camera.set_projection_matrices(width=self.width, height=self.height)
        GL.glViewport(0, 0, self.width, self.height)


if __name__ == "__main__":
    app = App()
    app.setup()
    if app.active:
        app.run()
    if isinstance(app, App):
        app.close()
    app = None
    del app
