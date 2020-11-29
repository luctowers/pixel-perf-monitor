import board
import supervisor
import displayio
from framebufferio import FramebufferDisplay
from rgbmatrix import RGBMatrix
from widgets import CpuWidget, GpuWidget, StorageWidget

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
gpu = GpuWidget(0, 9, matrix.width, primary_color=0x003000, secondary_color=0x000010, backlight_color=0x201010)
storage = StorageWidget(0, 18, matrix.width, primary_color=0xf01000, backlight_color=0x201010)
g.append(cpu)
g.append(gpu)
g.append(storage)
display.show(g)

def execute(instruction, arguments):
  if instruction == "cpu_usage":
    cpu.activity = list(map(float, arguments))
  elif instruction == "cpu_temperature":
    cpu.temperature = max(map(round, map(float, arguments)))
  elif instruction == "cpu_memory_usage":
    cpu.memory_usage = max(map(float, arguments))
  elif instruction == "gpu_usage":
    gpu.activity = max(map(float, arguments))
  elif instruction == "gpu_temperature":
    gpu.temperature = max(map(round, map(float, arguments)))
  elif instruction == "gpu_memory_usage":
    gpu.memory_usage = max(map(float, arguments))
  elif instruction == "storage_usage":
    storage.usage = max(map(float, arguments))
  elif instruction == "storage_read_throughput":
    storage.read_throughput = sum(map(float, arguments))
  elif instruction == "storage_write_throughput":
    storage.write_throughput = sum(map(float, arguments))

while True:
  display.refresh(target_frames_per_second=60, minimum_frames_per_second=0)
  while supervisor.runtime.serial_bytes_available:
    command = input().split()
    if command:
      try:
        execute(command[0], command[1:])
      except Exception as e:
        print(e)
