import board
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

cpu.activity = [0.0, 0.5, 1.0, 0.3]
cpu.memory_usage = 0.6
cpu.temperature = 65
gpu.activity = 0.4
gpu.memory_usage = 0.35
gpu.temperature = 49

while True:
  display.refresh(target_frames_per_second=10)
