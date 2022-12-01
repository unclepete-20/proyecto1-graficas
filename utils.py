import struct

def char(c):
    # 1 byte
    return struct.pack('=c',c.encode('ascii'))

def word(w):
    # 2  bytes
    return struct.pack('=h',w)

def dword(d):
    #4 bytes
    return struct.pack('=l', d)

def color(r, g, b):
  return bytes([round(b),round(g),round(r)])

unpack = lambda buffer: struct.unpack("=l", buffer)[0]

# Función que convierte coordenadas absolutas a relativas.
def absolute_to_relative_conversion(x, y, width, height):
  cx, cy = (width // 2), (height // 2)
  px, py = ((x - cx) / cx), ((y - cy) / cy)
  return px, py


BLACK = color(0, 0, 0)
WHITE = color(255, 255, 255)
RED = color(255, 0, 0)
GREEN = color(0, 255, 0)
BLUE = color(0, 0, 255)
