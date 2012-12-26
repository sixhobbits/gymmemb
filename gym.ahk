#SingleInstance,Force

#IfWinExist Gym Membership - Index
WinClose Gym Membership - Index
Sleep,1000
#IfWinExist

run, c:/users/Gareth/Desktop/gymmemb/index.py
WinWaitActive ahk_class ConsoleWindowClass
run, http://localhost:5000
WinWaitActive Gym Membership - Index
Send,{F11}
run, block.ahk, workingDir
return
