import displayio
from graphics import FractionRect
from fonts import MINISTAT_FONT
from adafruit_display_text.label import Label

class ProcessingUnitWidget(displayio.Group):

  def __init__(self, x, y, width, primary_color, secondary_color, font_color, label):
    self._label_graphic = Label(MINISTAT_FONT, text=label, color=font_color, anchor_point=(0.0,0.0), anchored_position=(1,1))
    self._temperature = 0
    self._temperature_graphic = Label(MINISTAT_FONT, text="--℃", color=font_color, anchor_point=(1.0,0.0), anchored_position=(width,1))
    self._memory_usage_graphic = FractionRect(0, 8, width, 1, primary_color, secondary_color)
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

  def __init__(self, x, y, width, primary_color, secondary_color, font_color):
    super().__init__(x, y, width, primary_color, secondary_color, font_color, "CPU")
    self._activity_graphic = FractionRect(0, 0, width, 7, primary_color, secondary_color)
    self.insert(0, self._activity_graphic)

  @property
  def activity(self):
    return self._activity_graphic.value

  @activity.setter
  def activity(self, value):
    self._activity_graphic.value = value

class GpuWidget(ProcessingUnitWidget):

  def __init__(self, x, y, width, primary_color, secondary_color, font_color):
    super().__init__(x, y, width, primary_color, secondary_color, font_color, "GPU")
    self._activity_graphic = FractionRect(0, 0, width, 7, primary_color, secondary_color)
    self.insert(0, self._activity_graphic)

  @property
  def activity(self):
    return self._activity_graphic.value

  @activity.setter
  def activity(self, value):
    self._activity_graphic.value = value