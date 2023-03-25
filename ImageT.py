import easyocr
import pyautogui
import os
import time
import win32gui

def FindW():
    handle=win32gui.FindWindow(0,"雷電模擬器")
    if handle == 0:
        return None
    else:
        return win32gui.GetWindowRect(handle)


ProjectPath=os.path.dirname(os.path.abspath(__file__))
print('Project >>',ProjectPath)

print("5秒後開始")
time.sleep(5)
E=pyautogui.screenshot()
E.save(f"{ProjectPath}\\TR.png")
print(E)
EOCR=easyocr.Reader(['ch_tra'],gpu=False)

result=EOCR.readtext(f"{ProjectPath}\\TR.png")
print(result)

#while True:
    #print(FindW())
#    time.sleep(0.5)


#print(result)