import displayio

def resize_vector(vector, size):
  def compute(index):
    sample_begin = index / size * len(vector)
    sample_begin_i = int(sample_begin)
    sample_end = (index+1) / size * len(vector)
    sample_end_i = int(sample_end)
    if sample_begin_i == sample_end_i:
      return vector[sample_begin_i]
    else:
      sum = 0
      sum += vector[sample_begin_i] * (sample_begin_i - sample_begin + 1)
      if sample_end - sample_end_i != 0:
        sum += vector[sample_end_i] * (sample_end - sample_end_i)
      for i in range(sample_begin_i+1, sample_end_i):
        sum += vector[i]
      return sum / (sample_end - sample_begin)
  return [ compute(i) for i in range(size) ]

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
    begin = round(total * min(1, max(0, self._fraction)))
    end = round(total * min(1, max(0, fraction)))
    if begin < end:
      for i in range(begin, end):
        self._bitmap[i] = 1
    elif begin > end:
      for i in range(end, begin):
        self._bitmap[i] = 0
    self.transpose_xy, self.flip_x, self.flip_y = cached_transform
    self._fraction = fraction

class VectorRect(displayio.Group):

  def __init__(self, x, y, width, height, primary_color, secondary_color):
    self._vector = None
    super().__init__(max_size=width)
    for i in range(width):
      slice = ScalarRect(x+i, y, height, 1, primary_color, secondary_color)
      slice.transpose_xy = True
      slice.flip_x = True
      self.append(slice)

  @property
  def value(self):
    return self._vector

  @value.setter
  def value(self, vector):
    resized_vector = resize_vector(vector, len(self))
    for i in range(len(self)):
      self[i].value = resized_vector[i]
    self._vector = vector
