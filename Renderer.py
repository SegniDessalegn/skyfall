from this import s
from OpenGL import GL as gl
import glfw
import sys
from Aircraft import Aircraft
from Mesh import Material, Mesh
from Shader import Shader
from Camera import *
import glm
from PIL import Image as im
import numpy as np
from Texture import CubeMap
from lighting import LightSource
from model import Model
from scene import Scene


skyboxVertices = [
    # positions          
    -1.0,  1.0, -1.0,
    -1.0, -1.0, -1.0,
     1.0, -1.0, -1.0,
     1.0, -1.0, -1.0,
     1.0,  1.0, -1.0,
    -1.0,  1.0, -1.0,

    -1.0, -1.0,  1.0,
    -1.0, -1.0, -1.0,
    -1.0,  1.0, -1.0,
    -1.0,  1.0, -1.0,
    -1.0,  1.0,  1.0,
    -1.0, -1.0,  1.0,

     1.0, -1.0, -1.0,
     1.0, -1.0,  1.0,
     1.0,  1.0,  1.0,
     1.0,  1.0,  1.0,
     1.0,  1.0, -1.0,
     1.0, -1.0, -1.0,

    -1.0, -1.0,  1.0,
    -1.0,  1.0,  1.0,
     1.0,  1.0,  1.0,
     1.0,  1.0,  1.0,
     1.0, -1.0,  1.0,
    -1.0, -1.0,  1.0,

    -1.0,  1.0, -1.0,
     1.0,  1.0, -1.0,
     1.0,  1.0,  1.0,
     1.0,  1.0,  1.0,
    -1.0,  1.0,  1.0,
    -1.0,  1.0, -1.0,

    -1.0, -1.0, -1.0,
    -1.0, -1.0,  1.0,
     1.0, -1.0, -1.0,
     1.0, -1.0, -1.0,
    -1.0, -1.0,  1.0,
     1.0, -1.0,  1.0
]


class Renderer:
    
    previousFrameTime = 0.0
    lastXpos = 300
    lastYpos = 400
    first = True

    def __init__(self, title: str, width: int, height: int):
        self.models = []
        self.width = width
        self.height = height

        # Aircraft.camera = Aircraft.camera
        # Aircraft.camera = Camera(glm.vec3(0.0, 0.0, 1.0), glm.vec3(0.0, 0.0, 0.0))
        
        if not glfw.init():
            print("Failed to initialize glfw!")
            sys.exit(1)

        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 4)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 0)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        glfw.window_hint(glfw.RESIZABLE, False)
        
        self.window = glfw.create_window(self.width, self.height, title, None, None)
        if not self.window:
            print("Failed to create glfw window!!")
            glfw.terminate()
            sys.exit(1)
        glfw.make_context_current(self.window)
        glfw.set_window_pos(self.window, 0, 0)
        # User Input Handling
        glfw.set_key_callback(self.window, Renderer.key_callback)
        glfw.set_cursor_pos_callback(self.window, self.mouse_callback)
        # Used to evaluate the viewport transform
        gl.glViewport(0, 0, self.width, self.height)

        # Enable depth testing
        gl.glEnable(gl.GL_DEPTH_TEST)
        gl.glDepthFunc(gl.GL_LEQUAL)
        
        # Default shader
        shader = Shader("shaders/vShader.sdr", "shaders/fShader.sdr")
        self.scene = Scene(shader, Aircraft.camera)
        self.scene.projection = glm.perspective(45.0, self.width / self.height, 1, 1000000000)
        self.environment = None


    def configure_light_source(self, sources):
        for source in sources:
            self.scene.add_light_source(source)

    def start(self):
        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
        # gl.glEnable(gl.GL_CULL_FACE)
        glfw.set_input_mode(self.window, glfw.CURSOR, glfw.CURSOR_DISABLED)
        # gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_LINE)
        while not glfw.window_should_close(self.window):
            # Event Handling
            glfw.poll_events()

            # Time per frame
            currentFrameTime = glfw.get_time()
            Camera.deltaTime = currentFrameTime - Renderer.previousFrameTime
            # print(1/Camera.deltaTime*100, " FPS")
            Aircraft.camera.update()
            # Rendering commands go here
            
            gl.glClearColor(0.65, 0.80, 0.95, 1.0)
            gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

            # gl.glDepthMask(gl.GL_FALSE)
            # skybox_shader.bind()
            # self.scene.shader.bind()
            # viewLocation = gl.glGetUniformLocation(self.scene.shader.program_id, 'view')
            # view = glm.mat4(glm.mat3(Renderer.camera.view))
            # gl.glUniformMatrix4fv(viewLocation, 1, gl.GL_FALSE, glm.value_ptr(view))

            # projectionLocation = gl.glGetUniformLocation(skybox_shader.program_id, 'projection')
            # gl.glUniformMatrix4fv(projectionLocation, 1, gl.GL_FALSE, glm.value_ptr(self.projection))

            # modelLocation = gl.glGetUniformLocation(skybox_shader.program_id, 'model')
            # scale = glm.scale(glm.vec3(1000))
            # gl.glUniformMatrix4fv(modelLocation, 1, gl.GL_FALSE, glm.value_ptr(scale))
            # skybox_shader.unbind()
            # gl.glBindTexture(gl.GL_TEXTURE_CUBE_MAP, cubemap_texture)
            # cubemap_body.Draw(skybox_shader.program_id, None)
            # gl.glDepthMask(gl.GL_TRUE)

            self.scene.render()
            # self.scene.eye = Renderer.camera
                
            # Swapping the double buffers
            glfw.swap_buffers(self.window)

        glfw.terminate()
        sys.exit(0)

    def setupEnvironment(self, tblrfb):

        cubemap = CubeMap(tblrfb, 5)
        # print(cubemap.tex_id)
        global skyboxVertices
        m = Material()
        m.set_map_textures([cubemap])
        skybox = Mesh(1, skyboxVertices, [i for i in range(36)])
    
        skybox_model = Model()
        skybox_shader = Shader('shaders/skybox_vertex_shader.sdr','shaders/skybox_fragment_shader.sdr')
        skybox_model.background = True
        skybox_model.custom_shader(skybox_shader)
        skybox_model.scale_n_place(glm.vec3(0.0, 0.0, 0.0), glm.vec3(1))
        skybox_model.meshes.append(skybox)
        skybox_model.materials[1]=m
        self.environment = cubemap
        self.add_model(skybox_model)


    def add_model(self, model: Model):
        for mesh in model.meshes:
            model.materials[mesh.id].textures[self.environment.type]=self.environment
        self.scene.add_models(model)


    @staticmethod
    def key_callback(window, key, scancode, action, mode):
        if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
            glfw.set_window_should_close(window, True)
        if key == glfw.KEY_W and action == glfw.PRESS:
            keys[glfw.KEY_W] = True
        elif key == glfw.KEY_W and action == glfw.RELEASE:
            keys[glfw.KEY_W] = False

        if key == glfw.KEY_S and action == glfw.PRESS:
            keys[glfw.KEY_S] = True
        elif key == glfw.KEY_S and action == glfw.RELEASE:
            keys[glfw.KEY_S] = False

        if key == glfw.KEY_A and action == glfw.PRESS:
            keys[glfw.KEY_A] = True
        elif key == glfw.KEY_A and action == glfw.RELEASE:
            keys[glfw.KEY_A] = False

        if key == glfw.KEY_D and action == glfw.PRESS:
            keys[glfw.KEY_D] = True
        elif key == glfw.KEY_D and action == glfw.RELEASE:
            keys[glfw.KEY_D] = False

        if key == glfw.KEY_UP and action == glfw.PRESS:
            keys[glfw.KEY_UP] = True
        elif key == glfw.KEY_UP and action == glfw.RELEASE:
            keys[glfw.KEY_UP] = False

        if key == glfw.KEY_DOWN and action == glfw.PRESS:
            keys[glfw.KEY_DOWN] = True
        elif key == glfw.KEY_DOWN and action == glfw.RELEASE:
            keys[glfw.KEY_DOWN] = False
        
        if key == glfw.KEY_R and action == glfw.PRESS:
            keys[glfw.KEY_R] = True
        elif key == glfw.KEY_R and action == glfw.RELEASE:
            keys[glfw.KEY_R] = False
        
        if key == glfw.KEY_T and action == glfw.PRESS:
            keys[glfw.KEY_T] = True
        elif key == glfw.KEY_T and action == glfw.RELEASE:
            keys[glfw.KEY_T] = False

    # @staticmethodself
    def mouse_callback(self, window, xPos, yPos):
        pass
        # # print(xPos, yPos)
        # xOffSet, yOffSet = 0, 0
        # if Renderer.first:
        #     Renderer.first = False
        # else:
        #     xOffSet = xPos - Renderer.lastXpos
        #     yOffSet = Renderer.lastYpos - yPos

        # Renderer.lastXpos = xPos
        # Renderer.lastYpos = yPos

        # sensitivity = 0.05
        # xOffSet *= sensitivity
        # yOffSet *= sensitivity

        # Aircraft.camera.pitch += yOffSet
        # Aircraft.camera.yaw += xOffSet

        # if Aircraft.camera.pitch > 89.99:
        #     Aircraft.camera.pitch = 89.99
        # elif Aircraft.camera.pitch < -89.99:
        #     Aircraft.camera.pitch = -89.99

        # newTarget = glm.vec3(0.0)
        # newTarget.x = glm.cos(glm.radians(Aircraft.camera.pitch)) * glm.cos(glm.radians(Aircraft.camera.yaw))
        # newTarget.y = glm.sin(glm.radians(Aircraft.camera.pitch))
        # newTarget.z = glm.cos(glm.radians(Aircraft.camera.pitch)) * glm.sin(glm.radians(Aircraft.camera.yaw))

        # Aircraft.camera.cameraFront = glm.normalize(newTarget)
        # Aircraft.camera.cameraRight = glm.normalize(glm.cross(Aircraft.camera.cameraFront, Aircraft.camera.cameraUp))

