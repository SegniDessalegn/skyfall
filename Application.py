from Renderer import Renderer

import glm
from Shader import Shader

from lighting import SpotLight, PointLight, DirectionalLight
from model import Model


def main():
    renderer = Renderer("Learn OpenGL", 800, 800)
    
    dl = DirectionalLight(glm.vec3(1), glm.vec3(0.5), glm.vec3(0.5))
    # dl.setDirection(glm.vec3(0.0, 0.0, -1.0))
    dl.setDirection(glm.vec3(0.0, -1.0, 0.0))

    pl = PointLight(glm.vec3(1), glm.vec3(1), glm.vec3(1))
    pl.setPosition(glm.vec3(1450.0, -4500.0, 10000.0))
    pl.setAttenuation(1.0, 0.000001, 0.0000032)

    sl = SpotLight(glm.vec3(1), glm.vec3(1), glm.vec3(1))
    sl.setDirection(renderer.camera.cameraFront)
    sl.setAttenuation(1.0, 0.00001, 0.000032)
    sl.setUpCutoff(50, 60)
    sl.setPosition(renderer.camera.cameraPos)

    renderer.configure_light_source([dl])
    renderer.setupEnvironment([
        'resources/textures/right.jpg',
        'resources/textures/left.jpg',
        'resources/textures/top.jpg',
        'resources/textures/bottom.jpg',
        'resources/textures/back.jpg',
        'resources/textures/front.jpg',
    ])

    md2 = Model()
    md2.load_model('resources/models/Cyborg/cyborg.obj')
    md2.scale_n_place(glm.vec3(1000.0, -5090.0, 9950.0), glm.vec3(20))
    renderer.add_model(md2)


    # skydome = Model()
    # skydome.load_model('resources/models/dome/dome.obj')
    # # skydome.background = True
    # skydome.scale_n_place(glm.vec3(-245000.0, 0.0, -245000.0), glm.vec3(1000))
    # renderer.add_model(skydome)

    # weird_rock = Model()
    # weird_rock.load_model('resources/models/Weird_Rock/weird_rock.obj')
    # weird_rock.scale_n_place(glm.vec3(10.0, 10.0, 0.0), glm.vec3(0.01))
    # renderer.add_model(weird_rock)

    # skyfall_env = Model()
    # skyfall_env.load_model('resources/models/sykfall/skyfall_test.obj')
    # skyfall_env.scale_n_place(glm.vec3(-122500.0, -1000.0, -122500.0), glm.vec3(2000))
    # skyfall_env.set_orientation(glm.vec3(1.0, 0.0, 0.0), 180)
    # renderer.add_model(skyfall_env)

    # ocean = Model()
    # ocean.instances(49)
    # ocean.load_model('resources/models/Ocean/Ocean.obj')
    # ocean_shader = Shader('resources/models/Ocean/custom_shader/ocean_vertex_shader.sdr', 'resources/models/Ocean/custom_shader/ocean_fragment_shader.sdr')
    # ocean.custom_shader(ocean_shader)
    # ocean.scale_n_place(glm.vec3(1000.0, -10000.0, 0.0), glm.vec3(10000))
    # renderer.add_model(ocean)

    ocean_final = Model()
    ocean_final.instances(10000)
    ocean_final.load_model('resources/models/TEST/brick_wall.obj')
    ocean_shader = Shader('resources/models/Ocean/custom_shader/ocean_vertex_shader.sdr', 'resources/models/Ocean/custom_shader/ocean_fragment_shader.sdr')
    ocean_final.custom_shader(ocean_shader)
    ocean_final.scale_n_place(glm.vec3(1000.0, -5090.0, 9950.0), glm.vec3(500000.0))
    renderer.add_model(ocean_final)


    weird_aircraft = Model()
    weird_aircraft.make_POV()
    weird_aircraft.load_model('resources/models/Aircraft/E 45 Aircraft_obj.obj')
    weird_aircraft.scale_n_place(glm.vec3(1000.0, -5090.0, 9950.0), glm.vec3(10))
    renderer.add_model(weird_aircraft)

    renderer.start()


if __name__ == '__main__':
    main()


