import re
from monitoring import computer
from LibreHardwareMonitor import Hardware

# TODO find a better way to categorize sensors than by name
used_space_pattern = re.compile(r"Used Space")
read_rate_pattern = re.compile(r"Read Rate")
write_rate_pattern = re.compile(r"Write Rate")

class Storage:

  def __init__(self, hw):
    self.hw = hw
    self.update()
    self.used_space_sensor = None
    self.read_throughput_sensor = None
    self.read_throughput_sensor = None
    for sensor in hw.Sensors:
      if sensor.SensorType == Hardware.SensorType.Load:
        if used_space_pattern.fullmatch(sensor.Name):
          self.used_space_sensor = sensor
      elif sensor.SensorType == Hardware.SensorType.Throughput:
          if read_rate_pattern.fullmatch(sensor.Name):
            self.read_rate_sensor = sensor
          elif write_rate_pattern.fullmatch(sensor.Name):
            self.write_rate_sensor = sensor

  def update(self):
    self.hw.Update()

  def usage(self):
    if self.used_space_sensor:
      return self.used_space_sensor.Value / 100
    else:
      return None

  def write_throughput(self):
    if self.write_rate_sensor:
      return self.write_rate_sensor.Value
    else:
      return None

  def read_throughput(self):
    if self.read_rate_sensor:
      return self.read_rate_sensor.Value
    else:
      return None

storage_list = list(map(Storage, filter(lambda hw: hw.HardwareType == Hardware.HardwareType.Storage, computer.Hardware)))
