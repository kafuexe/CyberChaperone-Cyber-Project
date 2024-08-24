@echo off


:start
cls

set python_ver=312

python ./get-pip.py

cd \
cd \python%python_ver%\Scripts\

python.exe -m pip install --upgrade pip
pip3 install threading
pip3 install os
pip3 install pyautogui
pip3 install sockets
pip3 install customtkinter
pip3 install pillow
pip3 install keyboard
pip3 install scapy
pip3 install CTkMessagebox
pip3 install cryptography
pause
exit