import re
from monitoring import computer
from LibreHardwareMonitor import Hardware

# TODO find a better way to categorize sensors than by name
core_name_pattern = re.compile(r"GPU Core")
memory_name_pattern = re.compile(r"GPU Memory")

class GPU:

  def __init__(self, hw):
    self.hw = hw
    self.update()
    self.load_sensor = None
    self.temperature_sensor = None
    self.memory_load_sensor = None
    for sensor in hw.Sensors:
      if sensor.SensorType == Hardware.SensorType.Temperature:
        if core_name_pattern.fullmatch(sensor.Name):
          self.temperature_sensor = sensor
      elif sensor.SensorType == Hardware.SensorType.Load:
        if core_name_pattern.fullmatch(sensor.Name):
          self.load_sensor = sensor
        elif memory_name_pattern.fullmatch(sensor.Name):
          self.memory_load_sensor = sensor

  def update(self):
    self.hw.Update()

  def temperature(self):
    if self.temperature_sensor:
      return self.temperature_sensor.Value
    else:
      return None

  def usage(self):
    if self.load_sensor:
      return self.load_sensor.Value / 100
    else:
      return None

  def memory_usage(self):
    if self.load_sensor:
      return self.memory_load_sensor.Value / 100
    else:
      return None

gpu_list = list(map(GPU, filter(lambda hw: hw.HardwareType in [Hardware.HardwareType.GpuNvidia, Hardware.HardwareType.GpuAmd], computer.Hardware)))
