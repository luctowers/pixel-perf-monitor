import re
from monitoring import computer
from LibreHardwareMonitor import Hardware

# TODO find a better way to categorize sensors than by name
memory_name_pattern = re.compile(r"Memory")

class Memory:

  def __init__(self, hw):
    self.hw = hw
    self.update()
    self.ram_usage_sensor = None
    for sensor in hw.Sensors:
      if sensor.SensorType == Hardware.SensorType.Load:
        if memory_name_pattern.fullmatch(sensor.Name):
          self.ram_usage_sensor = sensor

  def update(self):
    self.hw.Update()

  def usage(self):
    if self.ram_usage_sensor:
      return self.ram_usage_sensor.Value / 100
    else:
      return None

memory_list = list(map(Memory, filter(lambda hw: hw.HardwareType == Hardware.HardwareType.Memory, computer.Hardware)))
