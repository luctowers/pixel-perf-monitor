import displayio
import math

class ScalarRect(displayio.TileGrid):

  def __init__(self, x, y, width, height, primary_color, secondary_color):
    self._fraction = 0
    self._bitmap = displayio.Bitmap(width, height, 2)
    self._palette = displayio.Palette(2)
    if secondary_color is None:
      self._palette.make_transparent(0)
    else:
      self._palette[0] = secondary_color
    if primary_color is None:
      self._palette.make_transparent(1)
    else:
      self._palette[1] = primary_color
    super().__init__(self._bitmap, pixel_shader=self._palette, x=x, y=y)

  @property
  def value(self):
    return self._fraction

  @value.setter
  def value(self, fraction):
    # caching and restoring the transforms shouldn't be needed
    # I'm pretty sure this a bug in displayio.Bitmap class
    cached_transform = self.transpose_xy, self.flip_x, self.flip_y
    self.transpose_xy, self.flip_x, self.flip_y = False, False, False
    total = self._bitmap.width * self._bitmap.height
    begin = math.ceil(total * min(1, max(0, self._fraction)))
    end = math.ceil(total * min(1, max(0, fraction)))
    if begin < end:
      for i in range(begin, end):
        self._bitmap[i] = 1
    elif begin > end:
      for i in range(end, begin):
        self._bitmap[i] = 0
    self.transpose_xy, self.flip_x, self.flip_y = cached_transform
    self._fraction = fraction

class SkewedDistributionRect(displayio.Group):

  def __init__(self, x, y, width, height, primary_color, secondary_color):
    self._vector = None
    super().__init__(x=x, y=y, max_size=height)
    for i in range(height):
      slice = ScalarRect(0, i, width, 1, primary_color, secondary_color)
      self.append(slice)

  @property
  def value(self):
    return self._vector

  @value.setter
  def value(self, vector):
    rows = [ 0 for y in range(len(self)) ]
    for scalar in vector:
      magnitude = len(self) * max(0, min(scalar, 1))
      magnitude_i = int(magnitude)
      magnitude_r = magnitude % 1
      for i in range(magnitude_i):
        rows[len(self)-i-1] += 1
      rows[len(self)-magnitude_i-1] += magnitude_r
    for i in range(len(self)):
      self[i].value = rows[i] / len(vector)
    self._vector = vector
