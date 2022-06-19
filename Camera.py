import math
import glm
import glfw

keys = {}
# keys[glfw.KEY_W] = True

class Camera:
    deltaTime = 1000.0

    def __init__(self, position: glm.vec3, target: glm.vec3):
        
        self.cameraPos = position
        
        self.cameraFront = glm.normalize(target - self.cameraPos)
        
        self.pitch = glm.degrees(math.asin(self.cameraFront.y))
        self.yaw = glm.degrees(math.atan2(self.cameraFront.x, self.cameraFront.z)+math.pi/2)
        
        self.cameraUp = glm.vec3(0.0, 1.0, 0.0)
        self.cameraRight = glm.normalize(glm.cross(self.cameraFront, self.cameraUp))
        self.view = glm.lookAt(self.cameraPos, self.cameraFront + self.cameraPos , self.cameraUp)
        
        self.roll = glm.degrees(math.asin(self.cameraUp.x))

    def setCoordinateSystem(self, target: glm.vec3):

        self.cameraFront = glm.normalize(target - self.cameraPos)
        
        self.pitch = glm.degrees(math.asin(self.cameraFront.y))
        self.yaw = glm.degrees(math.atan2(self.cameraFront.x, self.cameraFront.z)+math.pi/2)
        
        self.cameraUp = glm.vec3(0.0, 1.0, 0.0)
        self.cameraRight = glm.normalize(glm.cross(self.cameraFront, self.cameraUp))
        
        self.view = glm.lookAt(self.cameraPos, self.cameraFront + self.cameraPos , self.cameraUp)
        
        self.roll = glm.degrees(math.asin(self.cameraUp.x))

    
    def changeYaw(self, new_yaw: float):
        self.yaw  = new_yaw
        self.reCalculate()
    
    def changePitch(self, new_pitch: float):
        rotate = glm.rotate(new_pitch, self.cameraRight)
        self.cameraFront = glm.normalize(rotate * self.cameraFront)
        self.cameraUp = glm.normalize(rotate * self.cameraUp)
        
        self.pitch = glm.degrees(math.asin(self.cameraFront.y))
        self.view = glm.lookAt(self.cameraPos, self.cameraFront + self.cameraPos , self.cameraUp)
        
        
    def changeRoll(self, new_roll: float):
        rotate = glm.rotate(-new_roll, self.cameraFront)
        self.cameraRight = glm.normalize(rotate * self.cameraRight)
        self.cameraUp = glm.normalize(rotate * self.cameraUp)
        self.roll = glm.degrees(math.asin(self.cameraUp.x))
        
        self.view = glm.lookAt(self.cameraPos, self.cameraFront + self.cameraPos , self.cameraUp)


    def moveForward(self):
        self.cameraPos = self.cameraPos + 100 * Camera.deltaTime * self.cameraFront
        self.update()
        # self.reCalculate()
        
    def reCalculate(self):
        newTarget = glm.vec3(0.0)
        newTarget.x = glm.cos(glm.radians(self.pitch)) * glm.cos(glm.radians(self.yaw))
        newTarget.y = glm.sin(glm.radians(self.pitch))
        newTarget.z = glm.cos(glm.radians(self.pitch)) * glm.sin(glm.radians(self.yaw))
        
        newCameraUp = glm.vec3(0.0, 0.0, self.cameraUp.z)
        newCameraUp.x = glm.sin(glm.radians(self.roll))
        newCameraUp.y = glm.cos(glm.radians(self.roll))
        self.cameraUp = glm.normalize(newCameraUp)

        self.cameraFront = glm.normalize(newTarget)
        self.cameraRight = glm.normalize(glm.cross(self.cameraFront, self.cameraUp))
        # self.cameraRight = glm.normalize(glm.cross(self.cameraFront, Aircraft.camera.cameraUp))

        self.update()
        
    def update(self):
        # cameraSpeed =100* Camera.deltaTime
        # if keys.get(glfw.KEY_W, False):
        #     self.cameraPos += cameraSpeed * self.cameraFront
        # if keys.get(glfw.KEY_S, False):
        #     self.cameraPos -= cameraSpeed * self.cameraFront
        # if keys.get(glfw.KEY_A, False):
        #     self.cameraPos -= self.cameraRight * cameraSpeed
        # if keys.get(glfw.KEY_D, False):
        #     self.cameraPos += self.cameraRight * cameraSpeed
        # if keys.get(glfw.KEY_UP, False):
        #     self.cameraPos += self.cameraUp * cameraSpeed
        # if keys.get(glfw.KEY_DOWN, False):
        #     self.cameraPos -= self.cameraUp * cameraSpeed
        
        self.view = glm.lookAt(self.cameraPos, self.cameraFront + self.cameraPos, self.cameraUp)