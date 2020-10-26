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
cpu = CpuWidget(0, 0, matrix.width, primary_color=0xf00000, secondary_color=0x201010, font_color=0x000000)
gpu = GpuWidget(0, 9, matrix.width, primary_color=0x002000, secondary_color=0x201010, font_color=0x000000)
g.append(cpu)
g.append(gpu)
display.show(g)

while True:
    for pu in [cpu, gpu]:
        pu.activity = (pu.activity + 0.003) % 1.0
        pu.memory_usage = (pu.memory_usage + 0.02) % 1.0
        pu.temperature = (pu.temperature + 1) % 100
    display.refresh(target_frames_per_second=10)