import re
from monitoring import computer
from LibreHardwareMonitor import Hardware

# TODO find a better way to categorize sensors than by name
CORE_NAME_PATTERN = re.compile(r"CPU Core #[1-9][0-9]*")
CDD_NAME_PATTERN = re.compile(r"CCD[1-9][0-9]* \(Tdie\)")
PACKAGE_NAME = "CPU Package"

class CPU:

  def __init__(self, hw):
    self.hw = hw
    self.update()
    core_temperatures = []
    ccd_temperatures = []
    package_temperatures = []
    other_temperatures = []
    core_loads = []
    other_loads = []
    for sensor in hw.Sensors:
      if sensor.SensorType == Hardware.SensorType.Temperature:
        if CORE_NAME_PATTERN.fullmatch(sensor.Name):
          core_temperatures.append(sensor)
        elif CDD_NAME_PATTERN.fullmatch(sensor.Name):
          ccd_temperatures.append(sensor)
        elif sensor.Name == PACKAGE_NAME:
          package_temperatures.append(sensor)
        else:
          other_temperatures.append(sensor)
      if sensor.SensorType == Hardware.SensorType.Load:
        if CORE_NAME_PATTERN.fullmatch(sensor.Name):
          core_loads.append(sensor)
        else:
          other_loads.append(sensor)
    self.temperature_sensors = core_temperatures or ccd_temperatures or package_temperatures or other_temperatures
    self.load_sensors = core_loads or other_loads

  def update(self):
    self.hw.Update()

  def temperatures(self):
    return [ sensor.Value for sensor in self.temperature_sensors ]

  def usages(self):
    return [ sensor.Value / 100 for sensor in self.load_sensors ]

cpu_list = list(map(CPU, filter(lambda hw: hw.HardwareType == Hardware.HardwareType.Cpu, computer.Hardware)))
