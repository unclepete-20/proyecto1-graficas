class Matrix(object):

  # Método constructor de la clase Matrix.
  def __init__(self, rows):
    self.rows = rows

  # Sobreescritura de la suma de matrices.
  def __add__(self, other):
    return Matrix([[(self.rows[i][j] + other.rows[i][j]) for j in range(len(self.rows[0]))] for i in range(len(self.rows))])

  # Sobreescritura de la resta de matrices.
  def __sub__(self, other):
    return Matrix([[(self.rows[i][j] - other.rows[i][j]) for j in range(len(self.rows[0]))] for i in range(len(self.rows))])

  # Sobreescritura de la multiplicación de matrices.
  def __mul__(self, other):
    return Matrix([[sum((a * b) for a, b in zip(x_row, y_column)) for y_column in zip(*other.rows)] for x_row in self.rows])

  # Representación textual de la matriz.
  def __repr__(self):
    return str([row for row in self.rows])
