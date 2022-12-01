from renderer import Renderer
from texture import Texture
from vector import V3
from shaders import rock_shader, spruce_shader
import math


renderer = Renderer()
renderer.gl_create_window(1024, 1024)
renderer.gl_viewport(0, 0, 1024, 1024)
renderer.gl_look_at(V3(0, 0, 10), V3(0, 0, 0), V3(0, 1, 0))
renderer.gl_clear_color(0, 0, 0.02)
renderer.gl_clear()


background = Texture("./backgrounds/background.bmp")
renderer.gl_load_background(background.pixels)


cat_texture = Texture("./textures/cat_txs.bmp")
renderer.gl_load_texture(cat_texture)
renderer.gl_load_obj("./models/cat.obj", (-0.5, -0.95, 0), (0.7, 0.7, 1.5), (0, (-0.3 * (math.pi / 4)), 0))

soccer_texture = Texture("./textures/soccer.bmp")
renderer.gl_load_texture(soccer_texture)
renderer.gl_load_obj("./models/soccer_ball.obj", (0.4, -0.8, 0), (0.03, 0.03, 0), (0, 0, 0))

person_texture = Texture("./textures/patrik_skin.bmp")
renderer.gl_load_texture(person_texture)
renderer.gl_load_obj("./models/Patrick.obj", (0.8, -0.6, -1), (0.4, 0.4, 0.5), (0, (-1 * (math.pi / 4)), 0))

alfred_texture = Texture("./textures/man.bmp")
renderer.gl_load_texture(alfred_texture)
renderer.gl_load_obj("./models/man.obj", (0, -0.6, -1), (0.05, 0.02, 0.03), (0, (-2 * (math.pi / 4)), 0))

forniture_texture = Texture("./textures/mask_txs.bmp")
renderer.gl_load_texture(forniture_texture)
renderer.gl_load_obj("./models/mask.obj", (-0.7, 0.2, -1), (1, 1, 0.2), (0, (0 * (math.pi / 4)), 0))

renderer.gl_load_shader(rock_shader)
renderer.gl_load_obj("./models/rock.obj", (-0.6, -0.5, 0.5), (0.003, 0.003, 0.003), ((math.pi / 6), 0, 0))


renderer.gl_load_shader(spruce_shader)
renderer.gl_load_obj("./models/spruce.obj", (-0.7, -0.5, -0.5), (-0.1, 1.5, 0.035), (((-1 * math.pi) / 2), 0, 0))


renderer.gl_finish("proyecto1.bmp")

