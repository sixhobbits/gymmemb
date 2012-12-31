#SingleInstance,Force

#IfWinExist Gym Membership - Index
WinClose Gym Membership - Index
Sleep,1000
#IfWinExist

run, index.exe, workingDir
WinWaitActive ahk_class ConsoleWindowClass
run, http://localhost:5000
WinWaitActive ahk_class Chrome_WidgetWin_1
Send,{F11}
run, block.exe, workingDir
return
