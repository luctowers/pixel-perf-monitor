$ErrorActionPreference="Inquire"
$scripts=Split-Path $MyInvocation.MyCommand.Path
$circuitpy_version="5.x"
& "$scripts\util\install-adafruit-lib.ps1" Adafruit_CircuitPython_Display_Text 2.9.2 $circuitpy_version
& "$scripts\util\install-adafruit-lib.ps1" Adafruit_CircuitPython_Bitmap_Font 1.2.2 $circuitpy_version
