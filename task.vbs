' Runs *.bat file without showing console window
' from https://www.winhelponline.com/blog/run-bat-files-invisibly-without-displaying-command-prompt/#:~:text=Running%20.BAT%20or%20.CMD%20files%20hidden%20(invisible%20mode)%20Using%20Script
Set WshShell = CreateObject("WScript.Shell") 
WshShell.Run chr(34) & "C:\Users\JonRobinson\Documents\dev\pyqt-timesheet\task.bat" & Chr(34), 0
Set WshShell = Nothing