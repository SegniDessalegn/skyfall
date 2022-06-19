

import math
from socket import AI_ADDRCONFIG
from model import Model
from Camera import Camera, keys
import glfw
import glm


class Aircraft(Model):
    roll_angle = 0
    pitch_angle = 0
    vertical_rotation_angle = 0
    camera = Camera(glm.vec3(1000.0, -5000.0, 10000.0), glm.vec3(1000.0, -10000.0, 0.0))
    def __init__(self) -> None:
        super().__init__()
        
    def update(self, shader_id: int):
        if keys.__contains__(glfw.KEY_S) and keys[glfw.KEY_S]:
            self.rotate("up")
            
        # elif keys.__contains__(glfw.KEY_W) and not keys[glfw.KEY_W]:
            # self.restore_rotation("up")
            # Aircraft.pitch_angle = 0
            
        if keys.__contains__(glfw.KEY_W) and keys[glfw.KEY_W]:
            self.rotate("down")
            
        # elif keys.__contains__(glfw.KEY_S) and not keys[glfw.KEY_S]:
        #     self.restore_rotation("down")
            # Aircraft.pitch_angle = 0
            
        if keys.__contains__(glfw.KEY_D) and keys[glfw.KEY_D]:
            self.rotate("right")
            
        # elif keys.__contains__(glfw.KEY_D) and not keys[glfw.KEY_D]:
        #     self.restore_rotation("right")
            
        if keys.__contains__(glfw.KEY_A) and keys[glfw.KEY_A]:
            self.rotate("left")
            
        # elif keys.__contains__(glfw.KEY_A) and not keys[glfw.KEY_A]:
        #     self.restore_rotation("left")
        
        x, y, z = self.location
        Aircraft.camera.cameraPos = self.location
        self.scale_n_place(glm.vec3(x, y + 100*glm.sin(Aircraft.pitch_angle), z - 100*glm.cos(Aircraft.pitch_angle)), self.scale)
        
        self.set_orientation(-Aircraft.camera.cameraFront, glm.degrees(Aircraft.roll_angle))
        # self.set_orientation(Aircraft.camera.cameraRight,  glm.degrees(Aircraft.pitch_angle))

        Aircraft.camera.setCoordinateSystem(self.location)
        Aircraft.camera.changeRoll(Aircraft.roll_angle)
        super().update(shader_id)
        

    def rotate(self, direction):
        if direction == "right":
            Aircraft.roll_angle -= 0.1
            
        elif direction == "left":
            Aircraft.roll_angle += 0.1
            
        if direction == "up":
            Aircraft.pitch_angle += 0.1
        if Aircraft.vertical_rotation_angle < 0.5 and Aircraft.vertical_rotation_angle > -0.5:
            Aircraft.vertical_rotation_angle += 0.1
            
        elif direction == "down":
            Aircraft.pitch_angle += -0.1
            if Aircraft.vertical_rotation_angle < 0.5 and Aircraft.vertical_rotation_angle > -0.5:
                Aircraft.vertical_rotation_angle -= 0.1