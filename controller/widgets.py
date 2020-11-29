import displayio
from graphics import ScalarRect, SkewedDistributionRect
from fonts import MINISTAT_FONT
from adafruit_display_text.label import Label

class ProcessingUnitWidget(displayio.Group):

  def __init__(self, x, y, width, primary_color, secondary_color, backlight_color, label):
    self._label_graphic = Label(MINISTAT_FONT, text=label, color=0x000000, anchor_point=(0.0,0.0), anchored_position=(1,1))
    self._temperature = 0
    self._temperature_graphic = Label(MINISTAT_FONT, text="--℃", color=0x000000, anchor_point=(1.0,0.0), anchored_position=(width,1))
    self._memory_usage_graphic = ScalarRect(0, 7, 2, width, secondary_color, backlight_color)
    self._memory_usage_graphic.transpose_xy = True
    self._memory_usage_graphic.flip_x = True
    super().__init__(x=x, y=y)
    self.append(self._memory_usage_graphic)
    self.append(self._temperature_graphic)
    self.append(self._label_graphic)

  @property
  def memory_usage(self):
    return self._memory_usage_graphic.value

  @memory_usage.setter
  def memory_usage(self, value):
    self._memory_usage_graphic.value = value

  @property
  def temperature(self):
    return self._temperature

  @temperature.setter
  def temperature(self, value):
    value = max(0, min(99, value))
    self._temperature_graphic.text = "%02d℃" % value
    self._temperature = value

class CpuWidget(ProcessingUnitWidget):

  def __init__(self, x, y, width, primary_color, secondary_color, backlight_color):
    super().__init__(x, y, width, primary_color, secondary_color, backlight_color, "CPU")
    self._activity_graphic = SkewedDistributionRect(0, 0, width, 7, primary_color, backlight_color)
    self.insert(0, self._activity_graphic)

  @property
  def activity(self):
    return self._activity_graphic.value

  @activity.setter
  def activity(self, value):
    self._activity_graphic.value = value

class GpuWidget(ProcessingUnitWidget):

  def __init__(self, x, y, width, primary_color, secondary_color, backlight_color):
    super().__init__(x, y, width, primary_color, secondary_color, backlight_color, "GPU")
    self._activity_graphic = ScalarRect(0, 0, width, 7, primary_color, backlight_color)
    self._activity_graphic.flip_y = True
    self.insert(0, self._activity_graphic)

  @property
  def activity(self):
    return self._activity_graphic.value

  @activity.setter
  def activity(self, value):
    self._activity_graphic.value = value

class StorageWidget(displayio.Group):

  def __init__(self, x, y, width, primary_color, backlight_color):
    self._left_text_graphic = Label(MINISTAT_FONT, text="--%", color=0x000000, anchor_point=(0.0,0.0), anchored_position=(1,1))
    self._right_text_graphic = Label(MINISTAT_FONT, text="0000", color=0x000000, anchor_point=(1.0,0.0), anchored_position=(width,1))
    self._storage_usage_graphic = ScalarRect(0, 0, 7, width, primary_color, backlight_color)
    self._storage_usage_graphic.transpose_xy = True
    self._storage_usage_graphic.flip_x = True
    super().__init__(x=x, y=y)
    self.append(self._storage_usage_graphic)
    self.append(self._left_text_graphic)
    self.append(self._right_text_graphic)
    self._read_throughput = 0
    self._write_throughput = 0

  @property
  def usage(self):
    return self._storage_usage_graphic.value

  @usage.setter
  def usage(self, value):
    self._storage_usage_graphic.value = value
    self._left_text_graphic.text = "%02d%%" % round(max(0, min(99, value * 100)))

  @property
  def read_throughput(self):
    return self._read_throughput

  @read_throughput.setter
  def read_throughput(self, value):
    self._read_throughput = value
    self.update_throughput_text()

  @property
  def write_throughput(self):
    return self._storage_usage_graphic.value

  @write_throughput.setter
  def write_throughput(self, value):
    self._write_throughput = value
    self.update_throughput_text()

  def update_throughput_text(self):
    self._right_text_graphic.text = "%04d" % round(max(0, min(9999, max(self._read_throughput, self._write_throughput) / 1000000)))
