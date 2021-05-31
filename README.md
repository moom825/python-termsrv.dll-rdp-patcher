# Py-RDP-Patcher
Py-RDP-Patcher is a tool  made in python to patch the termsrv file to allow simultaneous RDP sessions

## **Setup Guide:**
Install requirements :
```
pip3 install -r requirements.txt or pip install -r requirements.txt
```
Then if steps above were succesful after launching the python file by doing ```python patcher.py```
**Requirements:**\
Python3, Windows

**Limitations:**\
For now this script only supports windows 10 version 1909,1903,1809,1803 and 1703 (to know your version type this into powershell ```Get-ComputerInfo | select WindowsProductName, WindowsVersion```)  if your windows version is not supported and you know the corresponding hex code you can modify this script to support your version. I will not go into details on how to do it but the script is pretty straightforward if you know just a bit of python it should be easy to do.
