$ErrorActionPreference="Inquire"
$root=Split-Path (Split-Path $MyInvocation.MyCommand.Path)
$volumes=@(Get-Volume -FileSystemLabel CIRCUITPY)
if ($volumes.Count -eq 1) {
  if ($volumes[0].DriveLetter -eq "C") {
    throw "The C:\ drive probably shouldn't be named 'CIRCUITPY'."
  } else {
    Robocopy "$root\controller\" "$($volumes[0].DriveLetter):/" /MIR
  }
} else {
  throw "There must be exactly one volume labeled 'CIRCUITPY'."
}
