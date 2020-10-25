import displayio

class FractionRect(displayio.TileGrid):

    def __init__(self, x, y, width, height, fg=0xFFFFFF, bg=None):
        self._fraction = 0
        self._bitmap = displayio.Bitmap(height, width, 2)
        self._palette = displayio.Palette(2)
        if bg is None:
            self._palette.make_transparent(0)
        else:
            self._palette[0] = bg
        if fg is None:
            self._palette.make_transparent(1)
        else:
            self._palette[1] = fg
        super().__init__(self._bitmap, pixel_shader=self._palette, x=x, y=y)
        self.transpose_xy = True

    @property
    def value(self):
        return self._fraction

    @value.setter
    def value(self, fraction):
        # caching and restoring the transpose value shouldn't be needed
        # I'm pretty sure this a bug in displayio.Bitmap class
        cached_tranpose = self.transpose_xy
        self.transpose_xy = False
        fraction = min(1, max(0, fraction))
        total = self._bitmap.width * self._bitmap.height
        begin = round(total * self._fraction)
        end = round(total * fraction)
        if begin < end:
            for i in range(begin, end):
                self._bitmap[i] = 1
        elif begin > end:
            for i in range(end, begin):
                self._bitmap[i] = 0
        self._fraction = fraction
        self.transpose_xy = cached_tranpose