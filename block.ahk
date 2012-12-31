#Persistent
#SingleInstance,Force
MouseMove 0,A_ScreenHeight
BlockInput,MouseMove


; block all control input
^+Esc::
^!Delete::
F5::
LAlt::
RAlt::
LWin::
RWin::
RCtrl::
LCtrl::
LButton::
RButton::
MButton::
XButton1::
XButton2::
WheelUp::
WheelDown::
Esc::
Tab::
return
$F11::return ; Allow full-screen mode to be exited by simulated keystroke

CapsLock & Space::
^+q::
WinClose Gym Membership - Index
WinClose ahk_class ConsoleWindowClass
ExitApp

