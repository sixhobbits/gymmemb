run, c:/users/Gareth/Desktop/gymmemb/manage.py
WinWaitActive ahk_class ConsoleWindowClass
run, http://localhost:5000
WinWaitActive Gym Membership - Manage
Send,{F11}
return

^+q::
WinClose Gym Membership - Manage
WinClose ahk_class ConsoleWindowClass
ExitApp
