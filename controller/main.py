import board
import displayio
import terminalio
from framebufferio import FramebufferDisplay
from rgbmatrix import RGBMatrix
from adafruit_bitmap_font import bitmap_font
from adafruit_display_text.label import Label
from graphics import FractionRect

MINISTAT_FONT = bitmap_font.load_font("/ministat.bdf")

displayio.release_displays()
matrix = RGBMatrix(
    width=32, height=32, bit_depth=4,
    rgb_pins=[board.D6, board.D5, board.D9, board.D11, board.D10, board.D12],
    addr_pins=[board.A5, board.A4, board.A3, board.A2],
    clock_pin=board.D13, latch_pin=board.D0, output_enable_pin=board.D1
)
display = FramebufferDisplay(matrix, auto_refresh=False)

g = displayio.Group()
f = FractionRect(0, 0, matrix.width, 7, fg=0x001000, bg=0x201010)
l = Label(MINISTAT_FONT, text="GPU 42℃", color=0x000000, x=1, y=4)
g.append(f)
g.append(l)
display.show(g)

f.value = 0.42

while True:
    display.refresh(target_frames_per_second=10)