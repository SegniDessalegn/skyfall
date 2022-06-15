



from Mesh import Material
from Texture import Texture
from model import Model

class Ocean(Model):

    def __init__(self, m) -> None:
        super().__init__()
        self.normal_maps = []
        self.displacement_maps = []
        self.current_map = 0
        self.diffuse = m

    def load_normal_map_animation(self, directory: str, count: int):
        for i in range(1, count):
            map = Texture(directory+"normal_"+'0'*(4-len(str(i)))+str(i)+".png", "NORMAL", 1)
            self.normal_maps.append(map)
                

    def load_displacement_map_animation(self, directory: str, count: int):
        for i in range(1, count):
            map = Texture(directory+"disp_"+'0'*(4-len(str(i)))+str(i)+'.png', "DISPLACEMENT", 2)
            self.displacement_maps.append(map)
    
    def draw(self, shader_id: int):
        super().draw(shader_id)
        m = Material()
        m.set_map_textures([self.diffuse, self.normal_maps[self.current_map], self.displacement_maps[self.current_map]])
        self.materials[1] = m


