$WshShell = New-Object -comObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut("$Home\Desktop\Screen Time Tracker.lnk")
$Shortcut.TargetPath = "$PSScriptRoot\dist\ScreenTimeTracker.exe"
$Shortcut.Arguments = ""
$Shortcut.WorkingDirectory = "$PSScriptRoot"
$Shortcut.Description = "Screen Time Tracker - All-in-One"
$Shortcut.Save()

Write-Host "Desktop shortcut created successfully!"
Write-Host "You can now run Screen Time Tracker from your desktop."
