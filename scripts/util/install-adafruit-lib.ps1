param($library, $library_version, $circuitpy_version)
$root=Split-Path (Split-Path (Split-Path $MyInvocation.MyCommand.Path))
$package="$($library.ToLower().Replace('_','-'))-$circuitpy_version-mpy-$library_version"
$archive="$package.zip"
Invoke-WebRequest "https://github.com/adafruit/$library/releases/download/$library_version/$archive" -OutFile "$root/$archive"
Expand-Archive "$root/$archive" -DestinationPath $root
Remove-Item -Force "$root\$archive"
Copy-item -Force -Recurse "$root\$package\lib\*" -Destination "$root\controller\lib\"
Remove-Item -Force -Recurse "$root\$package"
