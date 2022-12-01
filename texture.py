"""
Universidad del Valle de Guatemala
(CC2018) Gráficas por Computadora
Librería de archivos .bmp
Santiago Taracena Puga (20017)
"""

# Módulos utilizados para el desarrollo de la clase Texture.
import utils
import bmp

# Definición de la clase Texture.
class Texture(object):

  # Método constructor de la clase Texture.
  def __init__(self, path):
    self.width, self.height, self.pixels = bmp.read_bmp(path)

  # Función para obtener un pixel en las coordenadas x e y de la imagen.
  def __get_x_and_y(self, tx, ty):
    return round(tx * self.width), round(ty * self.height)

  # Método para obtener el color de un pixel del archivo.
  def get_color(self, tx, ty):
    x, y = self.__get_x_and_y(tx, ty)
    return self.pixels[y][x]

  # Método para pobtener el color de un pixel con una intensidad dada.
  def get_color_with_intensity(self, tx, ty, intensity):

    # Obtención de los colores en x y en y.
    x, y = self.__get_x_and_y(tx, ty)

    # Nuevos colores con la intensidad aplicada.
    try:
      b, g, r = (
        round(self.pixels[y][x][0] * intensity),
        round(self.pixels[y][x][1] * intensity),
        round(self.pixels[y][x][2] * intensity),
      )
    except:
      b, g, r = 255, 255, 255

    # Retorno del color con su respectiva intensidad.
    return utils.color(r, g, b)
