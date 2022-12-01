"""
Universidad del Valle de Guatemala
(CC2018) Gráficas por Computadora
Librería de archivos .bmp
Santiago Taracena Puga (20017)
"""

# Módulos necesarios.
import struct

# Funciones lambda extra utilizadas.
color = lambda r, g, b: bytes([b, g, r])
char = lambda character: struct.pack("=c", character.encode("ascii"))
word = lambda word: struct.pack("=h", word)
dword = lambda dword: struct.pack("=l", dword)
unpack = lambda buffer: struct.unpack("=l", buffer)[0]

# Función que convierte coordenadas absolutas a relativas.
def absolute_to_relative_conversion(x, y, width, height):
  cx, cy = (width // 2), (height // 2)
  px, py = ((x - cx) / cx), ((y - cy) / cy)
  return px, py

# Constantes extra utilizadas.
BLACK = color(0, 0, 0)
WHITE = color(255, 255, 255)
RED = color(255, 0, 0)
GREEN = color(0, 255, 0)
BLUE = color(0, 0, 255)
