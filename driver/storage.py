import re
from monitoring import computer
from LibreHardwareMonitor import Hardware

# TODO find a better way to categorize sensors than by name
USED_SPACE_NAME = "Used Space"
READ_RATE_NAME = "Read Rate"
WRITE_RATE_NAME = "Write Rate"

class Storage:

  def __init__(self, hw):
    self.hw = hw
    self.update()
    self.used_space_sensor = None
    self.read_throughput_sensor = None
    self.read_throughput_sensor = None
    for sensor in hw.Sensors:
      if sensor.SensorType == Hardware.SensorType.Load:
        if sensor.Name == USED_SPACE_NAME:
          self.used_space_sensor = sensor
      elif sensor.SensorType == Hardware.SensorType.Throughput:
          if sensor.Name == READ_RATE_NAME:
            self.read_rate_sensor = sensor
          elif sensor.Name == WRITE_RATE_NAME:
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
