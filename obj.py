class Obj(object):

  # Método constructor de la clase Obj.
  def __init__(self, filename):

    # Lectura de todas las líneas del archivo .obj.
    with open(filename) as file:
      self.lines = file.read().splitlines()

    # Definición de las caras y los vértices del archivo.
    self.faces = []
    self.vertices = []
    self.texture_vertices = []
    self.normal_vertices = []
    self.__read_obj_lines()

  # Método que obtiene las caras y los vértices del archivo .obj.
  def __read_obj_lines(self):

    # Iteración sobre cada línea del archivo.
    for line in self.lines:

      # Si la longitud de la línea es menor a tres, no es una línea útil.
      if (len(line.split(" ")) < 3):
        continue

      # Prefijo y valor de cada línea útil del archivo.
      prefix, value = line.split(" ", 1)
      value = value.strip()

      # Obtención de las caras del archivo.        
      if (prefix == "f"):
        self.faces.append([list(map(int, face.split("/"))) for face in value.split(" ")])

      # Obtención de los vértices del archivo.
      elif (prefix == "v"):
        self.vertices.append(list(map(float, value.split(" "))))

      # Obtención de los vértices de texturas del archivo.
      elif (prefix == "vt"):
        self.texture_vertices.append(list(map(float, value.split(" "))))

      # Obtención de los vértices de normales del archivo.
      elif (prefix == "vn"):
        self.normal_vertices.append(list(map(float, value.split(" "))))
