import re
from monitoring import computer
from LibreHardwareMonitor import Hardware

# TODO find a better way to categorize sensors than by name
core_name_pattern = re.compile(r"CPU Core #[1-9][0-9]*")
ccd_name_pattern = re.compile(r"CCD[1-9][0-9]* \(Tdie\)")
package_name_pattern = re.compile(r"CPU Package")

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
        if core_name_pattern.fullmatch(sensor.Name):
          core_temperatures.append(sensor)
        elif ccd_name_pattern.fullmatch(sensor.Name):
          ccd_temperatures.append(sensor)
        elif package_name_pattern.fullmatch(sensor.Name):
          package_temperatures.append(sensor)
        else:
          other_temperatures.append(sensor)
      if sensor.SensorType == Hardware.SensorType.Load:
        if core_name_pattern.fullmatch(sensor.Name):
          core_loads.append(sensor)
        else:
          other_loads.append(sensor)
    self.temperature_sensors = core_temperatures or ccd_temperatures or package_temperatures or other_temperatures
    self.load_sensors = core_loads or other_loads

  def update(self):
    self.hw.Update()

  def temperatures(self):
    return [ sensor.Value for sensor in self.temperature_sensors ]

  def loads(self):
    return [ sensor.Value for sensor in self.load_sensors ]

cpu_list = list(map(CPU, filter(lambda hw: hw.HardwareType == Hardware.HardwareType.Cpu, computer.Hardware)))
