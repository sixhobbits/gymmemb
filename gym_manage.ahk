#SingleInstance, Force
run, manage.exe, workingDir
WinWaitActive ahk_class ConsoleWindowClass
run, http://localhost:5000
WinWaitActive ahk_class Chrome_WidgetWin_1
Send,{F11}
return

^+q::
Capslock & Space::
WinClose ahk_class Chrome_WidgetWin_1
WinClose ahk_class ConsoleWindowClass
ExitApp
