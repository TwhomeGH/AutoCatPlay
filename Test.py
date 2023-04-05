def log(*msg):
    """log 接收多個參數並打印
    
    使用方法:log(value1,value2,value..)
    value1,value2,value.. 可以是任何值可以一直往後增加
    """
    list(map(print,msg))
    
from CatFeed import *

import cv2

import pyautogui
import os,numpy

File_Root=os.path.abspath(os.path.dirname(__file__))
log(f'>> {File_Root}')

#圖片
TestFile=os.path.join(File_Root,"Test")
"""測試用資料夾"""

img=os.path.join(TestFile,"ORBTest.png")
"""螢幕畫面"""


ORB_Root=os.path.join(File_Root,"img")
"""專用測試資料夾ORB"""

#檢測圖
imgFind=os.path.join(ORB_Root,f"Gold.png") 
imgOut=numpy.zeros_like(img,dtype=numpy.float32) #輸出結果用


#讀取

imgFindR=cv2.imread(imgFind)

Rect=WinTool.FindW(Window='雷電模擬器')


while True:
    #截圖

    if Rect is None:
        continue
    RectL=Rect[2] 
    RectL=(RectL[0],RectL[1],int(RectL[2]-RectL[0]),int(RectL[3]-RectL[1]))

    print(f"{RectL}")
    pyautogui.screenshot(region=RectL).save(img)
    
    img1=cv2.imread(img)
    
    
    SIFTRes=cv2Tool.Search(img1,imgFindR)
    print(f"{len(SIFTRes[0])}")
    if len(SIFTRes[0])>=1:
        KP1=SIFTRes[1][0]
        KP2=SIFTRes[1][1]
        FindP=KP2[0][SIFTRes[0][0][0].trainIdx].pt
        print(f'找到的點:{FindP}')
        
        imgWH=(RectL[0],RectL[1])
        Find_T=(int(FindP[0]*0.95),int(FindP[1]*0.95),int(FindP[0]*0.1),int(FindP[1]*0.2))

        PFP=(imgWH[0]+Find_T[0],imgWH[1]+Find_T[1],int(Find_T[2]),int(Find_T[3]))
        
        print(f'Region:{PFP}')
        pyautogui.screenshot(region=PFP).save(f'{TestFile}\\ResF.png')
        ResS=cv2.imread(f'{TestFile}\\ResF.png')
        cv2.circle(ResS, (int(FindP[0])-Find_T[0],int(FindP[1])-Find_T[1]),5,(151, 204, 255),-1)
        
        cv2Tool.ShowImage(ResS,'FindResult')

        img2 = cv2.drawMatchesKnn(imgFindR, KP1[0],img1,KP2[0], SIFTRes[0],matchColor=(255, 199, 110),outImg=imgOut,flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
        cv2.imwrite(f"{TestFile}\\SQIF.png",img2)

        imgR=cv2.resize(img2, (960,540))

        cv2Tool.ShowImage(imgR,"keypoint")
    
    time.sleep(1)


