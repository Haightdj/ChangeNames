# ChangeNames
This repository contains a python program which will find/replace strings within filenames of a chosen folder

ChangeNames.py is the main program. 

Running this will launch a GUI interface where user and input (or path to)
a folder location, an old string that they would like to search for, and a new string that they would like to 
replace the old string with. There is a "preview" checkbox. when checked, changes will be shown in the 
faux-terminal window, but filenames will not be changed. The "clear" button clears the output form the faux-terminal
window. 

ui_ChangeNames.py is the GUI portion of the program that ChangeNames.py loads. Must be in same directory.

ui_ChangeNames.ui is the file produced using QT Designer

Current Reported Issues:

"Recently I’ve run into this problem a few times: After a certain period of time, it will stop changing names but won’t give any indication that the issue is because there are no files with that name. As pictured below, name changing was successful up until NAME REDACTED’s data. After that, I attempted a couple more changes that were unsuccessful. The program recognizes the command but doesn’t take action. Any idea why this may be happening? Closing and re-opening hasn’t worked in the past, but restarting the computer has. "
