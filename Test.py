def log(*msg):
    """log 接收多個參數並打印
    
    使用方法:log(value1,value2,value..)
    value1,value2,value.. 可以是任何值可以一直往後增加
    """
    list(map(print,msg))
    
from CatFeed import *

import matplotlib
import matplotlib.pyplot as plt
import cv2
import pyautogui
import os,numpy

matplotlib.use("TkAgg",force=True)

File_Root=os.path.abspath(os.path.dirname(__file__))
log(f'>> {File_Root}')
# log(WinTool.NowTime())

# def Test():
#     print("1")
#     print("2")
#     print("3")
    

# WinTool.Thread(Test)

#圖片
TestFile=os.path.join(File_Root,"Test") #測試用資料夾

img=os.path.join(TestFile,"ORBTest.png") #螢幕畫面

Num=1

ORB_Root=os.path.join(File_Root,"img","ORB") #專用測試資料夾ORB
#檢測圖
imgFind=os.path.join(ORB_Root,f"ADD_{Num}.png") 
imgOut=numpy.zeros_like(img,dtype=numpy.float32) #輸出結果用

#讀取

imgFindR=cv2.imread(imgFind)

ORB=cv2.SIFT_create()


matcher=cv2.BFMatcher()

Rect=WinTool.FindW(Window='雷電模擬器')

while True:
    #截圖
    
    RectL=Rect[2] 
    RectL=(RectL[0],RectL[1],int(RectL[2]-RectL[0]),int(RectL[3]-RectL[1]))

    print(f"{RectL}")
    pyautogui.screenshot(region=RectL).save(img)
    img1=cv2.imread(img)
    #比較截圖
    #比較用圖
    imgFindR=cv2.imread(os.path.join(ORB_Root,f"ADD_{Num}.png"))
    kp1,des1=ORB.detectAndCompute(imgFindR,None)
    kp2,des2=ORB.detectAndCompute(img1,None)
    matcher_bf=matcher.knnMatch(des1,des2,k=2)
    
    good=[]
    for m,n in matcher_bf:
        if m.distance < 0.75*n.distance:
            good.append([m])
    

    if len(good)>=4:
        FindP=kp2[good[2][0].trainIdx].pt
        print(f'找到的點:{FindP}')
        imgWH=(RectL[0],RectL[1])
        Find_T=(int(FindP[0]*0.9),int(FindP[1]*0.9),int(FindP[0]*0.2),int(FindP[1]*0.3))

        PFP=(imgWH[0]+Find_T[0],imgWH[1]+Find_T[1],int(Find_T[2]),int(Find_T[3]))
        
        print(f'Region:{PFP}')
        pyautogui.screenshot(region=PFP).save(f'{TestFile}\\ResF.png')
        ResS=cv2.imread(f'{TestFile}\\ResF.png')
        cv2.circle(ResS, (int(FindP[0])-Find_T[0],int(FindP[1])-Find_T[1]),10,(151, 204, 255),-1)
        cv2.imshow('FindResult',ResS)
        cv2.waitKey(3000)
        cv2.destroyAllWindows()


    print(f'找到的數量:{len(good)}')
    img2 = cv2.drawMatchesKnn(imgFindR, kp1,img1,kp2, good,matchColor=(255, 199, 110),outImg=imgOut,flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
    cv2.imwrite(f"{TestFile}\\SQIF.png",img2)

    imgR=cv2.resize(img2, (960,540))
    cv2.imshow("keypoints", imgR)
    cv2.waitKey(3000)
    cv2.destroyAllWindows()
    
    Num+=1
    if Num>2:Num=1
    good.clear()
    log(f":{imgFind}")
    time.sleep(1)


