import pyautogui
from pynput import keyboard
import time
import os

ProjectPath=os.path.abspath(os.path.dirname(__file__))
print(ProjectPath)
Save=os.path.join(ProjectPath,"Shot")

temp=[pyautogui.position(),pyautogui.position()]


def GetC(xy1,xy2):
    print("取樣開始")
    temp2=[]
    for i in range(10):
        print(f"取樣第{i+1}張")
        xy3,xy4=((xy2.x-xy1.x),(xy2.y-xy1.y))
        Scr=pyautogui.screenshot(region=(xy1.x,xy1.y,xy3,xy4))
        Scr.save(os.path.join(Save,f"{i+1}.png"))
        temp2.append(f"{i+1}.png")
        time.sleep(30)

    print(f"列表:\n{temp2}")   



def key(key):
    if key == keyboard.Key.esc:
        print(f"終止程序:{key}")
        os._exit(0)
    if key == keyboard.KeyCode.from_char('g'):
        temp[0]=pyautogui.position()
        print(f"座標1:{temp[0]}")
    if key == keyboard.KeyCode.from_char('h'):
        temp[1]=pyautogui.position()
        print(f"座標2:{temp[1]}")
    if key == keyboard.KeyCode.from_char('o'):
        print("開始取樣於5秒後")
        time.sleep(5)
        GetC(temp[0],temp[1])
        
    print(key,type(key))



#鍵盤監聽開啟
KeyL=keyboard.Listener(on_press=key)
KeyL.start()

use="""
按 G設置 取樣點1
按 H設置 取樣點2
"""

print(use)

while True:
    print(pyautogui.position())
    time.sleep(1)