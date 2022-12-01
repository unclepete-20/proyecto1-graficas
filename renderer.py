from obj import Obj
from vector import V3
from camera import Camera
import utils
import bmp
import math


class Renderer(object):

  def __init__(self, width=1000, height=1000):
    self.__width = width
    self.__height = height
    self.__viewport_width = 0
    self.__viewport_height = 0
    self.__viewport_x_coordinate = 0
    self.__viewport_y_coordinate = 0
    self.__background_color = utils.BLACK
    self.__current_color = utils.WHITE
    self.__framebuffer = []
    self.__z_buffer = [[-999_999 for x in range(self.__width)] for y in range(self.__height)]
    self.__texture = None
    self.__camera = Camera()
    self.__active_shader = None
    self.__light = V3(0, 0, -1)
    self.gl_clear()

  
  def gl_clear(self):
    self.__framebuffer = [[(self.__background_color) for x in range(self.__width)] 
                          for y in range(self.__height)]

  
  def gl_clear_color(self, r, g, b):
    self.__background_color = utils.color(
      math.ceil(r * 255),
      math.ceil(g * 255),
      math.ceil(b * 255),
    )

  
  def gl_color(self, r, g, b):
    self.__current_color = utils.color(
      math.ceil(r * 255),
      math.ceil(g * 255),
      math.ceil(b * 255),
    )

  
  def gl_create_window(self, width, height):
    self.__width = width
    self.__height = height
    self.gl_clear()

  
  def gl_viewport(self, x, y, width, height):
    self.__viewport_x_coordinate = round(x)
    self.__viewport_y_coordinate = round(y)
    self.__viewport_width = round(width)
    self.__viewport_height = round(height)
    for w in range(self.__viewport_width):
      for h in range(self.__viewport_height):
        self.__framebuffer[self.__viewport_y_coordinate + h][self.__viewport_x_coordinate + w] = self.__background_color

  
  def gl_reset_framebuffer(self, new_framebuffer=[]):
    self.__framebuffer = new_framebuffer

  
  def __relative_to_absolute_conversion(self, x, y):
    cx, cy = (self.__viewport_width // 2), (self.__viewport_height // 2)
    px, py = (round((x + 1) * cx) + self.__viewport_x_coordinate), (round((y + 1) * cy) + self.__viewport_y_coordinate)
    return px, py

  
  def gl_vertex(self, x, y):
    if ((0 < x < self.__viewport_width) and (0 < y < self.__viewport_height)):
      self.__framebuffer[y][x] = self.__current_color

  
  def gl_absolute_vertex(self, x, y):
    if ((0 <= x <= self.__width) and (0 <= y <= self.__height)):
      self.__framebuffer[y + self.__viewport_y_coordinate][x + self.__viewport_x_coordinate] = self.__current_color

  
  def gl_relative_vertex(self, x, y):
    if ((-1 <= x <= 1) and (-1 <= y <= 1)):
      px, py = self.__relative_to_absolute_conversion(x, y)
      self.__framebuffer[px][py] = self.__current_color

  
  def gl_line(self, x0, y0, x1, y1):

    
    x0, y0, x1, y1 = round(x0), round(y0), round(x1), round(y1)

    
    dy = abs(y1 - y0)
    dx = abs(x1 - x0)

    
    steep = (dy > dx)

   
    if (steep):
      x0, y0 = y0, x0
      x1, y1 = y1, x1

    # Cambio de variables para el orden de dibujo de la línea.
    if (x0 > x1):
      x0, x1 = x1, x0
      y0, y1 = y1, y0

    # Nuevo cálculo de los diferenciales de la línea.
    dy = abs(y1 - y0)
    dx = abs(x1 - x0)

    # Variables importantes para dibujar.
    offset = 0
    threshold = dx
    y = y0

    # Iteración sobre los puntos de la línea.
    for x in range(x0, (x1 + 1)):

      # Dibujo de la línea.
      if (steep):
        self.gl_vertex(x, y)
      else:
        self.gl_vertex(y, x)

      # Recálculo del offset.
      offset += (dy * 2)

      # Cambio del threshold cuando el offset es mayor.
      if (offset >= threshold):
        y += 1 if (y0 < y1) else -1
        threshold += dx * 2

  # Función que dibuja una línea con coordenadas relativas.
  def gl_relative_line(self, x0, y0, x1, y1):
    if ((-1 <= x0 <= 1) and (-1 <= y0 <= 1) and (-1 <= x1 <= 1) and (-1 <= y1 <= 1)):
      x0, y0 = self.__relative_to_absolute_conversion(x0, y0)
      x1, y1 = self.__relative_to_absolute_conversion(x1, y1)
      self.gl_line(x0, y0, x1, y1)

  # Función que calcula si un punto está dentro de un polígono.
  def __is_inside(self, x, y, polygon):

    # Variables útiles para el proceso.
    result = False
    vertices = len(polygon)
    value = (vertices - 1)

    # Iteración sobre cada vértice del polígono.
    for i in range(vertices):

      # Descarte de puntos que sean parte de las líneas fronterizas del polígono.
      if ((x == polygon[i][0]) and (y == polygon[i][1])):
        return True

      # Evaluación de la elevación de cada punto del polígono.
      if ((polygon[i][1] > y) != (polygon[value][1] > y)):

        # Cálculo de la pendiente entre los dos puntos.
        upper_slope_component = ((x - polygon[i][0]) * (polygon[value][1] - polygon[i][1]))
        lower_slope_component = ((polygon[value][0] - polygon[i][0]) * (y - polygon[i][1]))
        slope = (upper_slope_component - lower_slope_component)

        # Si la pendiente es cero, el punto está dentro.
        if (slope == 0):
          return True

        # Si las pendientes siguen siendo diferentes, recalculamos el resultado.
        elif ((slope < 0) != (polygon[value][1] < polygon[i][1])):
          result = not result

      # Cambio de vértice actual.
      value = i

    # Retorno del resultado.
    return result

  # Función que dibuja y colorea un polígono de puntos dados.
  def gl_fill_polygon(self, polygon):
    for x in range(self.__width):
      for y in range(self.__height):
        if (self.__is_inside(x, y, polygon)):
          self.gl_vertex(x, y)

  # Función que carga y dibuja un archivo .obj.
  def gl_load_obj(self, obj_file, translate_factor, scale_factor, rotate_factor, color=None):

    # Carga de la matriz de modelo de la cámara con los factores dados a gl_load_obj().
    self.__camera.load_model_matrix(V3(*translate_factor), V3(*scale_factor), V3(*rotate_factor))

    # Nueva definición del color del modelo.
    if (color is None):
      color = (1, 1, 1)

    # Carga y lectura del archivo .obj.
    object_file = Obj(obj_file)

    # Iteración sobre cada cara del archivo .obj.
    for face in object_file.faces:

      # Dibujo de un cuadrado.
      if (len(face) == 4):

        # Cálculo de las caras del cuadrado.
        first_face = (abs(face[0][0]) - 1)
        second_face = (abs(face[1][0]) - 1)
        third_face = (abs(face[2][0]) - 1)
        fourth_face = (abs(face[3][0]) - 1)

        # Vértices del cuadrado a dibujar.
        first_vertex = self.__camera.transform_vertex(object_file.vertices[first_face])
        second_vertex = self.__camera.transform_vertex(object_file.vertices[second_face])
        third_vertex = self.__camera.transform_vertex(object_file.vertices[third_face])
        fourth_vertex = self.__camera.transform_vertex(object_file.vertices[fourth_face])

        # Carga de texturas si hay una textura activa para el modelo.
        if (self.__texture):

          # Cálculo de las caras del cuadrado.
          first_texture_face = (face[0][1] - 1)
          second_texture_face = (face[1][1] - 1)
          third_texture_face = (face[2][1] - 1)
          fourth_texture_face = (face[3][1] - 1)

          # Vértices de la textura cargada.
          first_texture_vertex = V3(*object_file.texture_vertices[first_texture_face])
          second_texture_vertex = V3(*object_file.texture_vertices[second_texture_face])
          third_texture_vertex = V3(*object_file.texture_vertices[third_texture_face])
          fourth_texture_vertex = V3(*object_file.texture_vertices[fourth_texture_face])

          # Vectores normales si el modelo tiene normales.
          if (object_file.normal_vertices):

            # Cálculo de las normales de las caras del cuadrado.
            first_normal_face = (face[0][2] - 1)
            second_normal_face = (face[1][2] - 1)
            third_normal_face = (face[2][2] - 1)
            fourth_normal_face = (face[3][2] - 1)

            # Vértices de la textura cargada.
            first_normal_vertex = V3(*object_file.normal_vertices[first_normal_face])
            second_normal_vertex = V3(*object_file.normal_vertices[second_normal_face])
            third_normal_vertex = V3(*object_file.normal_vertices[third_normal_face])
            fourth_normal_vertex = V3(*object_file.normal_vertices[fourth_normal_face])

          else:
            first_normal_vertex = V3(0, 0, 0)
            second_normal_vertex = V3(0, 0, 0)
            third_normal_vertex = V3(0, 0, 0)
            fourth_normal_vertex = V3(0, 0, 0)

          # Triángulo superior del cuadrado texturizado.
          self.gl_draw_triangle(
            (first_vertex, second_vertex, third_vertex),
            (first_texture_vertex, second_texture_vertex, third_texture_vertex),
            (first_normal_vertex, second_normal_vertex, third_normal_vertex)
          )

          # Triángulo inferior del cuadro texturizado.
          self.gl_draw_triangle(
            (fourth_vertex, first_vertex, third_vertex),
            (fourth_texture_vertex, first_texture_vertex, third_texture_vertex),
            (fourth_normal_vertex, first_normal_vertex, third_normal_vertex)
          )

        # Polígonos a dibujar si no hay una textura.
        else:
          self.gl_draw_triangle((first_vertex, second_vertex, third_vertex), color=color)
          self.gl_draw_triangle((first_vertex, third_vertex, fourth_vertex), color=color)

      # Dibujo de un triángulo.
      elif (len(face) == 3):

        # Cálculo de las caras del triángulo.
        first_face = (abs(face[0][0]) - 1)
        second_face = (abs(face[1][0]) - 1)
        third_face = (abs(face[2][0]) - 1)

        # Vértices del triángulo a dibujar.
        first_vertex = self.__camera.transform_vertex(object_file.vertices[first_face])
        second_vertex = self.__camera.transform_vertex(object_file.vertices[second_face])
        third_vertex = self.__camera.transform_vertex(object_file.vertices[third_face])

        # Carga de texturas si hay una textura activa.
        if (self.__texture):

          # Cálculo de las caras del triángulo.
          first_texture_face = (face[0][1] - 1)
          second_texture_face = (face[1][1] - 1)
          third_texture_face = (face[2][1] - 1)

          # Vértices del triángulo a dibujar.
          first_texture_vertex = V3(*object_file.texture_vertices[first_texture_face])
          second_texture_vertex = V3(*object_file.texture_vertices[second_texture_face])
          third_texture_vertex = V3(*object_file.texture_vertices[third_texture_face])

          # Vectores normales si el modelo tiene normales.
          if (object_file.normal_vertices):

            # Cálculo de las normales de las caras del cuadrado.
            first_normal_face = (face[0][2] - 1)
            second_normal_face = (face[1][2] - 1)
            third_normal_face = (face[2][2] - 1)

            # Vértices de la textura cargada.
            first_normal_vertex = V3(*object_file.normal_vertices[first_normal_face])
            second_normal_vertex = V3(*object_file.normal_vertices[second_normal_face])
            third_normal_vertex = V3(*object_file.normal_vertices[third_normal_face])

          else:
            first_normal_vertex = V3(0, 0, 0)
            second_normal_vertex = V3(0, 0, 0)
            third_normal_vertex = V3(0, 0, 0)

          # Triángulo texturizado a dibujar.
          self.gl_draw_triangle(
            (first_vertex, second_vertex, third_vertex),
            (first_texture_vertex, second_texture_vertex, third_texture_vertex),
            (first_normal_vertex, second_normal_vertex, third_normal_vertex)
          )

        # Polígonos necesarios para el triángulo sin texturas.
        else:
          self.gl_draw_triangle((first_vertex, second_vertex, third_vertex), color=color)

  # Función que halla los límites de un triángulo a pintar.
  def __bounding_box(self, A, B, C):

    # Coordenadas de los vértices del triángulo.
    coords = [(A.x, A.y), (B.x, B.y), (C.x, C.y)]

    # Valores mínimos y máximos exagerados.
    xmin = 9999
    xmax = -9999
    ymin = 9999
    ymax = -9999

    # Cálculo de los nuevos máximos y mínimos.
    for (x, y) in coords:
      if (x < xmin):
        xmin = x
      if (x > xmax):
        xmax = x
      if (y < ymin):
        ymin = y
      if (y > ymax):
        ymax = y

    # Retorno de los vectores mínimos y máximos del triángulo.
    return V3(xmin, ymin), V3(xmax, ymax)

  # Función que calcula coordenadas baricéntricas.
  def __barycentric_coords(self, A, B, C, P):

    # V3 creado para el cálculo de las coordenadas.
    Vector = (V3((B.x - A.x), (C.x - A.x), (A.x - P.x)) * V3((B.y - A.y), (C.y - A.y), (A.y - P.y)))

    # Cálculo de los valores u, v y w resultantes.
    try:
      u = (Vector.x / Vector.z)
      v = (Vector.y / Vector.z)
      w = (1 - ((Vector.x + Vector.y) / Vector.z))
    except:
      u, v, w = -1, -1, -1

    # Retorno de los valores w, v y u.
    return (w, v, u)

  # Función que dibuja un triángulo dados tres puntos A, B y C.
  def gl_draw_triangle(self, points, texture_points=(V3(0, 0, 0), V3(0, 0, 0), V3(0, 0, 0)), normal_points=(V3(0, 0, 0), V3(0, 0, 0), V3(0, 0, 0)), color=None):

    # Puntos y texturas a dibujar con el triángulo.
    A, B, C = points[0], points[1], points[2]

    # Puntos obtenidos de las texturas cargadas.
    if (self.__texture):
      tA, tB, tC = texture_points

    if (self.__active_shader):
      nA, nB, nC = normal_points

    # V3 normal e intensidad del triángulo.
    normal = ((C - A) * (B - A))
    intensity = (self.__light.norm() @ normal.norm())

    # Si la intensidad es menor a cero, no dibujamos nada.
    if (intensity < 0):
      return

    # Cambio de color para colorear un modelo.
    if (color is not None):
      self.gl_color(color[0] * intensity, color[1] * intensity, color[2] * intensity)

    # Coloración en blanco y negro del modelo.
    else:
      self.gl_color(intensity, intensity, intensity)

    # Puntos mínimos y máximos sobre los cuáles dibujar.
    min_point, max_point = self.__bounding_box(A, B, C)
    min_point.round_coords()
    max_point.round_coords()

    # Iteración sobre el triángulo a pintar.
    for x in range(min_point.x, (max_point.x + 1)):
      for y in range(min_point.y, (max_point.y + 1)):

        # Coordenadas a pintar.
        w, v, u = self.__barycentric_coords(A, B, C, V3(x, y))

        # Casos en los que el punto no se encuentra en el triángulo.
        if ((w < 0) or (v < 0) or (u < 0)):
          continue

        # Cálculo de la coordenada z del triángulo a pintar.
        z = ((A.z * w) + (B.z * u) + (C.z * v))

        # Si el valor a pintar está frente al último valor del z-buffer, lo pintamos.
        if ((abs(x) < len(self.__z_buffer)) and (abs(y) < len(self.__z_buffer[0])) and (self.__z_buffer[x][y] < z)):

          # Definición de un nuevo valor del z-buffer.
          self.__z_buffer[x][y] = z

          # Coloración de un shader cargado.
          if (self.__active_shader):
            self.__current_color = self.__active_shader(
              x=x,
              y=y,
              width=self.__width,
              height=self.__height,
              light=self.__light,
              coords=(w, u, v),
              texture_coords=(tA, tB, tC),
              normal_coords=(nA, nB, nC)
            )

          # Coloración de una textura cargada.
          elif (self.__texture):
            tx = ((tA.x * w) + (tB.x * u) + (tC.x * v))
            ty = ((tA.y * w) + (tB.y * u) + (tC.y * v))
            self.__current_color = self.__texture.get_color_with_intensity(tx, ty, intensity)

          # Punto del triángulo a dibujar.
          self.gl_vertex(x, y)

  # Función que carga una textura para el modelo.
  def gl_load_texture(self, texture):
    self.__texture = texture

  # Función para determinar la dirección de la cámara del renderer.
  def gl_look_at(self, eye, center, up):
    z = (eye - center).norm()
    x = (up * z).norm()
    y = (z * x).norm()
    self.__camera.look_at(x, y, z, eye, center, self.__width, self.__height)

  # Función para cargar un shader al renderer.
  def gl_load_shader(self, shader):
    self.__active_shader = shader

  # Función para cargar un fondo al renderer.
  def gl_load_background(self, background):
    self.__framebuffer = background

  # Función para renderizar la imagen creada.
  def gl_finish(self, filename):    
    return bmp.write_bmp(filename, self.__framebuffer, self.__width, self.__height)
