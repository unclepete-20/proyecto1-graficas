from vector import V3
from matrix import Matrix
import math

class Camera(object):


  def __init__(self):
    self.__model_matrix = None
    self.__view_matrix = None
    self.__projection_matrix = None
    self.__viewport_matrix = None

  # Método para transformar un vértice con las matrices de la cámara.
  def transform_vertex(self, vertex):
    augmented_vertex = Matrix([[vertex[0]], [vertex[1]], [vertex[2]], [1]])
    transformed_vertex = (self.__viewport_matrix * self.__projection_matrix * self.__model_matrix * self.__view_matrix * augmented_vertex)
    rows = transformed_vertex.rows
    return V3((rows[0][0] / rows[3][0]), (rows[1][0] / rows[3][0]), (rows[2][0] / rows[3][0]))

  # Matriz de modelado para trasladar, escalar y rotar un modelo.
  def load_model_matrix(self, translate=V3(0, 0, 0), scale=V3(1, 1, 1), rotate=V3(0, 0, 0)):

    # Matriz de traslación en los ejes x, y y z.
    translation_matrix = Matrix([
      [1, 0, 0, translate.x],
      [0, 1, 0, translate.y],
      [0, 0, 1, translate.z],
      [0, 0, 0, 1]
    ])

    # Matrix para escalar el modelo al tamaño deseado.
    scale_matrix = Matrix([
      [scale.x, 0, 0, 0],
      [0, scale.y, 0, 0],
      [0, 0, scale.z, 0],
      [0, 0, 0, 1]
    ])    

    # Matriz para rotar el modelo en el eje x.
    rotation_x = Matrix([
      [1, 0, 0, 0],
      [0, math.cos(rotate.x), (-1 * math.sin(rotate.x)), 0],
      [0, math.sin(rotate.x), math.cos(rotate.x), 0],
      [0, 0, 0, 1]
    ])

    # Matriz para rotar el modelo en el eje y.
    rotation_y = Matrix([
      [math.cos(rotate.y), 0, math.sin(rotate.y), 0],
      [0, 1, 0, 0],
      [(-1 * math.sin(rotate.y)), 0, math.cos(rotate.y), 0],
      [0, 0, 0, 1]
    ])

    # Matriz para rotar el modelo en el eje z.
    rotation_z = Matrix([
      [math.cos(rotate.z), (-1 * math.sin(rotate.z)), 0, 0],
      [math.sin(rotate.z), math.cos(rotate.z), 0, 0],
      [0, 0, 1, 0],
      [0, 0, 0, 1]
    ])

    # Definición de la matriz de rotación y matriz de modelo.
    rotation_matrix = (rotation_x * rotation_y * rotation_z)
    self.__model_matrix = (translation_matrix * rotation_matrix * scale_matrix)

  # Método para cargar la matriz de vista de la cámara.
  def load_view_matrix(self, prime_x, prime_y, prime_z, center):

    # Matrix de componentes x, y y z.
    component_matrix = Matrix([
      [prime_x.x, prime_x.y, prime_x.z, 0],
      [prime_y.x, prime_y.y, prime_y.z, 0],
      [prime_z.x, prime_z.y, prime_z.z, 0],
      [0, 0, 0, 1]
    ])

    # Matriz de ajuste en el "cuarto eje" de las matrices.
    adjust_matrix = Matrix([
      [1, 0, 0, (-1 * center.x)],
      [0, 1, 0, (-1 * center.y)],
      [0, 0, 1, (-1 * center.z)],
      [0, 0, 0, 1]
    ])

    # Definición de la matriz de vista.
    self.__view_matrix = (component_matrix * adjust_matrix)

  # Método para cargar la matriz de proyección de la cámara.
  def load_projection_matrix(self, eye, center):

    # Coeficiente de proyección de la matriz.
    coefficient = (-1 / (eye.length() - center.length()))

    # Definición de la matriz de proyección.
    self.__projection_matrix = Matrix([
      [1, 0, 0, 0],
      [0, 1, 0, 0],
      [0, 0, 1, 0],
      [0, 0, coefficient, 1]
    ])

  # Método para cargar la matriz del viewport de la imagen.
  def load_viewport_matrix(self, width, height):

    # Coordenadas x e y del viewport, ancho y alto del mismo.
    x, y = 0, 0
    w, h = (width / 2), (height / 2)

    # Definición de la matriz del viewport de la imagen.
    self.__viewport_matrix = Matrix([
      [w, 0, 0, (x + w)],
      [0, h, 0, (y + h)],
      [0, 0, 128, 128],
      [0, 0, 0, 1]
    ])

  # Método para cambiar la dirección de la cámara y cargar las matrices de la misma.
  def look_at(self, x, y, z, eye, center, width, height):
    self.load_view_matrix(x, y, z, center)
    self.load_projection_matrix(eye, center)
    self.load_viewport_matrix(width, height)
