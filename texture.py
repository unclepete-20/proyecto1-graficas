import utils
import bmp


class Texture(object):


  def __init__(self, path):
    self.width, self.height, self.pixels = bmp.read_bmp(path)

  
  def __get_x_and_y(self, tx, ty):
    return round(tx * self.width), round(ty * self.height)

  
  def get_color(self, tx, ty):
    x, y = self.__get_x_and_y(tx, ty)
    return self.pixels[y][x]

  
  def get_color_with_intensity(self, tx, ty, intensity):

    
    x, y = self.__get_x_and_y(tx, ty)

    
    try:
      b, g, r = (
        round(self.pixels[y][x][0] * intensity),
        round(self.pixels[y][x][1] * intensity),
        round(self.pixels[y][x][2] * intensity),
      )
    except:
      b, g, r = 255, 255, 255

    
    return utils.color(r, g, b)
