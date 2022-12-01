import utils


def write_bmp(filename, framebuffer, width, height):
  
  # BMP FILE BYTES TO PROCESS IT
  FILE_HEADER_SIZE = 14
  IMAGE_HEADER_SIZE = 40
  HEADER_SIZE = (FILE_HEADER_SIZE + IMAGE_HEADER_SIZE)
  COLORS_PER_PIXEL = 3
  

  file = open(filename, "bw")

  
  file.write(utils.char("B"))
  file.write(utils.char("M"))
  file.write(utils.dword(HEADER_SIZE + (width * height * COLORS_PER_PIXEL)))
  file.write(utils.dword(0))
  file.write(utils.dword(HEADER_SIZE))

  
  file.write(utils.dword(IMAGE_HEADER_SIZE))
  file.write(utils.dword(width))
  file.write(utils.dword(height))
  file.write(utils.word(1))
  file.write(utils.word(24))
  file.write(utils.dword(0))
  file.write(utils.dword(width * height * COLORS_PER_PIXEL))
  file.write(utils.dword(0))
  file.write(utils.dword(0))
  file.write(utils.dword(0))
  file.write(utils.dword(0))

  
  for x in range(width):
    for y in range(height):
      file.write(framebuffer[x][y])

  
  file.close()

# Función que lee un archivo .bmp.
def read_bmp(path):

  # Apertura del archivo .bmp a leer.
  with open(path, "rb") as image:

    # Definición del ancho y alto de la imagen.
    image.seek(2 + 4 + 2 + 2)
    header_size = utils.unpack(image.read(4))
    image.seek(2 + 4 + 2 + 2 + 4 + 4)
    width = utils.unpack(image.read(4))
    height = utils.unpack(image.read(4))

    # Salto del header para leer los pixeles de la imagen.
    image.seek(header_size)

    # Lista de pixeles a retornar al finalizar el proceso.
    pixels = []

    # Iteración sobre todas las "filas" del archivo.
    for y in range(height):

      # Nueva fila de pixeles del archivo.
      pixels.append([])

      # Iteración sobre los pixeles de cada "fila".
      for _ in range(width):

        # Tonalidades azul, verde y roja del pixel leído.
        b, g, r = (ord(image.read(1)), ord(image.read(1)), ord(image.read(1)))

        # Almacenamiento del pixel en su respectiva posición en la lista.
        pixels[y].append(utils.color(r, g, b))

  # Retorno del ancho, alto y pixeles de la imagen.
  return width, height, pixels
