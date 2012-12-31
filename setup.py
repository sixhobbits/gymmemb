from cx_Freeze import setup,Executable

includefiles = [ 'templates\index.html','templates\checkmember.html','templates\memberok.html','templates\memberinvalid.html','members.db','templates\\namematches.html', 
				  'logs\init', 'templates\manage.html', 'templates\\authenticate.html', 'static', 'README.rtf']
includes = []
excludes = ['Tkinter']
base = "Win32GUI"

setup(
name = 'index',
version = '0.1',
description = 'membership app',
author = 'Me',
author_email = 'me@me.com',
options = {'build_exe': {'excludes':excludes,'include_files':includefiles}}, 
executables = [Executable('index.py'), Executable('manage.py')]
)

