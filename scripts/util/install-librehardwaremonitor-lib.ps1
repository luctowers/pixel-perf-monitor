param($version)
$root=Split-Path (Split-Path (Split-Path $MyInvocation.MyCommand.Path))
$package="LibreHardwareMonitor-$version-Binaries"
$archive="$package.zip"
Invoke-WebRequest "https://github.com/LibreHardwareMonitor/LibreHardwareMonitor/releases/download/v$version/Binaries.zip" -OutFile "$root\$archive"
Expand-Archive "$root\$archive" -DestinationPath "$root/$package"
Remove-Item -Force "$root\$archive"
Copy-item -Force "$root\$package\LibreHardwareMonitorLib.dll" -Destination "$root\driver\lib\"
Remove-Item -Force -Recurse "$root\$package"
