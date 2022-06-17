
from difflib import restore
from Renderer import Renderer
from model import Model
from Camera import keys
import glfw
import glm



class Aircraft(Model):
    restore_counter = 0
    rotate_angle = 0
    def __init__(self) -> None:
        super().__init__()
        
    def update(self, shader_id: int):
        super().update(shader_id)
        print(Aircraft.rotate_angle, Aircraft.restore_counter)
        if keys.__contains__(glfw.KEY_T) and keys[glfw.KEY_T]:
            self.rotate("right")
            self.set_orientation(glm.vec3(0, 0, -1), Aircraft.rotate_angle)
            print(self.axis, self.angle)
        elif keys.__contains__(glfw.KEY_T) and not keys[glfw.KEY_T]:
            self.restore_rotation("right")
            self.set_orientation([0, 0, -1], Aircraft.restore_counter)
        if keys.__contains__(glfw.KEY_R) and keys[glfw.KEY_R]:
            self.rotate("left")
            self.set_orientation(glm.vec3(0, 0, -1), Aircraft.rotate_angle)
            print(self.axis, self.angle)
        elif keys.__contains__(glfw.KEY_R) and not keys[glfw.KEY_R]:
            self.restore_rotation("left")
            self.set_orientation([0, 0, -1], Aircraft.restore_counter)

        super().update(shader_id)
    
    def rotate(self, direction):
        if direction == "right":
            Aircraft.restore_counter = Aircraft.rotate_angle
            Aircraft.rotate_angle += 1
        elif direction == "left":
            Aircraft.restore_counter = Aircraft.rotate_angle
            Aircraft.rotate_angle -= 1
    
    def restore_rotation(self, direction):
        if direction == "right":
            if Aircraft.restore_counter > 0:
                Aircraft.restore_counter -= 1
            if Aircraft.rotate_angle > 0:
                Aircraft.rotate_angle -= 1
        elif direction == "left":
            if Aircraft.restore_counter < 0:
                Aircraft.restore_counter += 1
            if Aircraft.rotate_angle < 0:
                Aircraft.rotate_angle += 1