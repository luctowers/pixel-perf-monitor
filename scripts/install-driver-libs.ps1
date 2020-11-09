$ErrorActionPreference="Inquire"
$scripts=Split-Path $MyInvocation.MyCommand.Path
pip install pyserial pythonnet
& "$scripts\util\install-librehardwaremonitor-lib.ps1" 0.8.5
