import re
from monitoring import computer
from LibreHardwareMonitor import Hardware

# TODO find a better way to categorize sensors than by name
DOWNLOAD_RATE_NAME = "Download Speed"
UPLOAD_RATE_NAME = "Upload Speed"

class Network:

  def __init__(self, hw):
    self.hw = hw
    self.update()
    self.used_space_sensor = None
    self.download_throughput_sensor = None
    self.upload_throughput_sensor = None
    for sensor in hw.Sensors:
      if sensor.SensorType == Hardware.SensorType.Throughput:
          if sensor.Name == DOWNLOAD_RATE_NAME:
            self.download_throughput_sensor = sensor
          elif sensor.Name == UPLOAD_RATE_NAME:
            self.upload_throughput_sensor = sensor

  def update(self):
    self.hw.Update()

  def usage(self):
    if self.used_space_sensor:
      return self.used_space_sensor.Value / 100
    else:
      return None

  def download_throughput(self):
    if self.download_throughput_sensor:
      return self.download_throughput_sensor.Value
    else:
      return None

  def upload_throughput(self):
    if self.upload_throughput_sensor:
      return self.upload_throughput_sensor.Value
    else:
      return None

network_list = list(map(Network, filter(lambda hw: hw.HardwareType == Hardware.HardwareType.Network, computer.Hardware)))
