import clr
import os

dll_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'lib\LibreHardwareMonitorLib.dll'))
clr.AddReference(dll_path)

from LibreHardwareMonitor import Hardware

computer = Hardware.Computer()
computer.IsCpuEnabled = True
computer.IsMemoryEnabled = True
computer.IsGpuEnabled = True
computer.IsStorageEnabled = True
computer.IsNetworkEnabled = True
computer.Open()

def update():
  for hw in computer.Hardware:
    hw.Update()
