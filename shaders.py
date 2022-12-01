import random
import utils


def plant_shader(**kwargs):

  # Parámetros necesarios para el shader.
  y = kwargs["y"]

  # Factor para el gradiente de la planta.
  y_factor = (1 - abs((160 - y) / 160))

  # Retorno del color con el gradiente incluido.
  return utils.color(30, round(150 * y_factor), 100)


def rock_shader(**kwargs):

  # Parámetros necesarios para el shader.
  y = kwargs["y"]

  # Factor vertical del color de la roca.
  y_factor = (1 - abs((400 - y) / 100))
  actual_factor = max(min(y_factor, 1), 0)


  random_value = random.random()


  if (random_value <= 0.05):
    return utils.color(10, 10, 10)
  elif ((0.05 < random_value <= 0.1) and (y > 360)):
    return utils.color(200, 200, 200)

  # Retorno del gris del gradiente vertical de la roca.
  return utils.color(round(75 * actual_factor), round(75 * actual_factor), round(75 * actual_factor))


def spruce_shader(**kwargs):

  # Parámetros necesarios para el shader.
  y = kwargs["y"]

  # Factor vertical del color del pino.
  y_factor = (1 - abs((425 - y) / 350))

  # Selección de un color aleatorio para frondosidad.
  if (random.random() < 0.1):
    return random.choice((
      utils.color(45, 145, 170),
      utils.color(50, 150, 175),
      utils.color(55, 155, 180),
      utils.color(60, 160, 185),
    ))


  return utils.color(50, round(150 * y_factor), round(175 * y_factor))
