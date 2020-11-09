import board
import supervisor
import displayio
from framebufferio import FramebufferDisplay
from rgbmatrix import RGBMatrix
from widgets import CpuWidget, GpuWidget

displayio.release_displays()
matrix = RGBMatrix(
  width=32, height=32, bit_depth=4,
  rgb_pins=[board.D6, board.D5, board.D9, board.D11, board.D10, board.D12],
  addr_pins=[board.A5, board.A4, board.A3, board.A2],
  clock_pin=board.D13, latch_pin=board.D0, output_enable_pin=board.D1
)
display = FramebufferDisplay(matrix, auto_refresh=False)

g = displayio.Group()
cpu = CpuWidget(0, 0, matrix.width, primary_color=0xf00000, secondary_color=0x000010, backlight_color=0x201010)
gpu = GpuWidget(0, 9, matrix.width, primary_color=0x002000, secondary_color=0x000010, backlight_color=0x201010)
g.append(cpu)
g.append(gpu)
display.show(g)

cpu.memory_usage = 0.6
gpu.activity = 0.4
gpu.memory_usage = 0.35
gpu.temperature = 49

while True:
  display.refresh(target_frames_per_second=60, minimum_frames_per_second=0)
  while supervisor.runtime.serial_bytes_available:
    command = input().split()
    if command:
      operation = command[0]
      arguments = command[1:]
      if operation == "cpu_load":
        cpu.activity = list(map(float, arguments))
      elif operation == "cpu_temperature":
        cpu.temperature = max(map(round,map(float, arguments)))
