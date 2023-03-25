import pyautogui
import pydirectinput #用於點擊
from pynput import keyboard,mouse #鍵盤事件用
import time #等待用
import os #用來取當前文件位置
import win32gui #窗口范範圍捕抓

import random
from CatFeed import GetItem

#import threading as Th #線程

#項目位置
ProjectPath=os.path.dirname(os.path.abspath(__file__))
print('Project >>',ProjectPath)

ESCCount=0
Delay=3 #檢測延遲
AutoNext=0 #自動下一步
AutoMode=[0,3,[0,0]] #用於確定是否需要自動接替
BackCount=0
AutoPlay=0
Region=(0,0,0,0) #查找位置
CaptureF=0

ItemGet=GetItem()

TestAddState=[
    '1.png', '2.png', '3.png', '4.png', '5.png', 
    '6.png', '7.png', '8.png', '9.png', '10.png',
    ]

os.system("title Auto加碼多多")



def CheckActiveWindow():
    """
    此方法獲取正在使用窗口信息\n
    返回 窗口標題 Text 標題長度 Len\n
        纇名 Class 窗口大小 Rect(x1,y1,x2,y2) 
    """
    ActWindow=win32gui.GetForegroundWindow() #取當前正在使用的窗口
    
    WindowLen=win32gui.GetWindowTextLength(ActWindow)
    if win32gui.GetWindowText(ActWindow) == "":
        WindowT="沒有窗口標題"
    else:
        WindowT=win32gui.GetWindowText(ActWindow)
    
    Result={
            "Text":WindowT,
            "Len":WindowLen,
            "Class":win32gui.GetClassName(ActWindow),
            "Rect":win32gui.GetWindowRect(ActWindow)
    }
    return Result

def WCall(hand,extra):
    """
    handle 句柄
    extra 格式設定
    """
    wind=extra
    temp=[]
    temp.append(win32gui.GetWindowText(hand))
    wind[hand]=temp
    print(f"{hand}:{extra}")

def FindW(Class=None,Window=None):
    """
    用於指定窗口定位\n
    Window 查找特定窗口名稱
    Class 纇名
    """
    handle=win32gui.FindWindow(Class,Window)
    if handle == 0:
        return None
    else:
        temp=[
            win32gui.GetClassName(handle),
            win32gui.GetWindowText(handle),
            handle
        ]
        return temp

def click(xy,num=1,x1r=0):
    """
    xy 位置
    x1r x偏易增減
    num 次數
    """
    for i in range(num):
        pydirectinput.mouseDown(xy[0]+x1r,xy[1])
        pydirectinput.mouseUp(xy[0]+x1r,xy[1]) 
        time.sleep( (random.randint(1,4)/10)+1)


def get_xy(img_path,name,tip=None,confi=0.9,regionS=None):
    """
    img_path 檢測圖片位置\n
    name 顯示名稱\n
    tip 提示沒有找到 1開啟 預設關閉\n
    """
    Add=os.path.join(ProjectPath,"img",img_path) #用於圖片查找位置存放

    #檢測圖片
    if regionS:
        Position=pyautogui.locateCenterOnScreen(image=Add,confidence=confi,region=regionS)
    else:
        Position=pyautogui.locateCenterOnScreen(image=Add,confidence=confi)
    

    if Position:
        print(f"{name} 找到了:{Position}")
        return Position
    elif tip==1:
        print(f"{name} 沒有")

def MoreSearch(dir="Add",listT=list(("1.png","2.png")),Name="Test"):
    """
    dir 設置所處資料夾
    """
    
    for i in listT:
        Num=listT.index(i)
        FindListT=get_xy(f"{dir}\\{listT[Num]}",Name)
        if FindListT:
            return FindListT
        else:
            return None

def press(key):
    """
    key 接收按下的按鍵
    鍵盤按鍵接收用
    """
    global BackCount,AutoPlay,AutoMode
    
    if AutoMode[0]==1:
        AutoMode[0]=0
    if AutoMode[1]<10:
        AutoMode[1]+=1
        
    
    if key == keyboard.Key.esc:
            BackCount+=1
            if BackCount>=5:
                print(ItemGet.Result())
                print('結束進程')
                os._exit(0)
    if key == keyboard.KeyCode.from_char('g'):
        if AutoPlay==0:
            AutoPlay=1
            print("啟用自動戰鬥簡易操作")
        else:
            AutoPlay=0
            print("關閉自動戰鬥")
    if key == keyboard.KeyCode.from_char('h'):
        print(pyautogui.position())        
    
    

def move(x,y):
    global AutoMode
    if AutoMode[0]==1:
        AutoMode[0]=0
    if AutoMode[1]<10:
        AutoMode[1]+=1
    #print(x,y)

#鍵盤按鍵接收
listen=keyboard.Listener(on_press=press)
listen.start()
#滑鼠移動檢測
listen2=mouse.Listener(on_move=move)
listen2.start()


while True:
    BackCount=0
    Position=pyautogui.position()
    PositionXY=[Position.x,Position.y]
    print(f"當前位置:{PositionXY} 延遲:{Delay} 狀態:{AutoMode[0]}")
    print(f"自動:{60-AutoNext} 接替於:{AutoMode[1]}")
    #LDOperationRecorderWindow 操作錄製窗口
    #LDPlayerMainFrame 主窗口
    
    #winF=win32console.GetConsoleWindow()
    #print(win32gui.IsIconic(winF),win32gui.IsChild(winF))
    
    
    AutoMode[1]-=1
    
    
    if AutoMode[1]<=0:
        AutoMode[0]=1

    HasRun=get_xy('HasRun.png',"正在遊戲中")    
    if HasRun and AutoPlay==1:
        Shot=get_xy("Play\\Shot3.png","貓咪炮")
        
        if Shot:
            Region=(HasRun.x,Shot.y-230,Shot.x,Shot.y)
            print(Region)
        if Region!=None:
            Squirrel=get_xy('Play\\AT\\BSquirrel.png',"黑松鼠")
            BlackCat=get_xy('Play\\AT\\BlackCat.png',"黑熊")

            if BlackCat:
                if Shot:keyboard.Events.Press('1')

            Cat=get_xy('Play\\1.png',"基本牆",regionS=Region)#基本牆
            Cat2=get_xy('Play\\2.png',"大狂牆",regionS=Region)#大狂牆
            Cat3=get_xy('Play\\3.png',"跳跳貓",regionS=Region)#跳跳貓
            Cat4=get_xy('Play\\4.png',"拉麵貓",regionS=Region)#拉麵貓
            Cat5=get_xy('Play\\5.png',"大狂鳥",regionS=Region)#大狂鳥

            if Squirrel:
                if Cat4:click(Cat4)
                if Cat5:click(Cat5)

            if Cat3:
                if Cat3:click(Cat3)
                if Cat2:click(Cat)
                if Cat:click(Cat2)

            if Cat or Cat2:
                if Cat:click(Cat)
                if Cat2:click(Cat2)
            
            if Cat4:
                time.sleep(2)
                click(Cat4)
            
            if Cat5:
                time.sleep(3)
                click(Cat5)   



    #ChWindow=FindW(Window="雷電模擬器")
    if AutoMode[0]==1:
        # if ItemGet.Rest == False:
        #     RunSet=get_xy("RunSet.png","關卡選擇")
        #     if RunSet and ItemGet:
        #         click(RunSet)
        #     Rest=get_xy("Other\\Rest.png","貓咪休息中")
        #     if Rest:
        #         ItemGet.Rest=True
        #         RestBack=get_xy("Other\\RestBack.png","休息回加碼多多")
        #         if RestBack:
        #             click(RestBack,x1r=376)
        #             time.sleep(10)
            

        #     CCRest=get_xy('Other\\CCRest.png',"貓咪元寶關卡")
        #     if CCRest:
        #         pydirectinput.mouseDown(CCRest[0],CCRest[1])
        #         pydirectinput.mouseUp(CCRest[0],CCRest[1]) 

        #     CCGet=get_xy("item\\CC+1.png","獲得1元寶")
        #     if CCGet:
        #         pydirectinput.mouseDown(CCGet[0],CCGet[1])
        #         pydirectinput.mouseUp(CCGet[0],CCGet[1]) 
        #         ItemGet.CC+=1
                
        #     BackB=get_xy("BackB.png","返回地圖")
        #     if BackB:
        #         pydirectinput.mouseDown(BackB[0],BackB[1])
        #         pydirectinput.mouseUp(BackB[0],BackB[1])
        #         time.sleep(5)    
        #     CC2=get_xy('Other\\CC2.png',"貓咪元寶關卡")
        #     if CC2:
        #         RunCC2=get_xy("RunCC2.png","運行元寶腳本")
        #         if RunCC2:
        #             pydirectinput.mouseDown(RunCC2[0]+376,RunCC2[1])
        #             pydirectinput.mouseUp(RunCC2[0]+376,RunCC2[1])
        #             time.sleep(5)
                    
            
        #     CantRun=get_xy("CantRun.png","無法進行")
        #     if CantRun:
        #         OK=get_xy("OK.png","確認")
        #         if OK:
        #             pydirectinput.mouseDown(OK[0],OK[1])
        #             pydirectinput.mouseUp(OK[0],OK[1])

        #     HasRun=get_xy("HasRun.png","正在遊戲中 頻率設為60秒")
        #     if HasRun:
        #         Delay=30
        #     else:
        #         Delay=5
        #         print(f"非遊戲中 頻率設定為{Delay}秒")
        
        # if ItemGet.Rest == True:
            #探險狀態
            if Delay>=60:
                Delay-=3
            
            Work1=get_xy("Work.png","加碼多多 正在探險")
            if Work1 == None: #非探險
                CNext=get_xy("Select\\NextCheck.png","可下一步")

                Cancel=get_xy("Cancel.png","關閉頁面")
                if Cancel:click(Cancel)

                Base=get_xy("Base.png","正在基地")
                if Base:
                    Addd=get_xy("Add4.png","去加碼多多")
                    if Addd:
                        click(Addd)
                
                if BackCount>=6:
                    if Base:
                        BackR=get_xy("Back2.png","返回基地")
                        click(BackR)
                    BackCount=0

                if CNext:
                    Delay=1
                    Card=get_xy("item\\Card.png","獲得貓咪卷")
                    if Card:
                        time.sleep(1)
                        OK=get_xy("OK3.png","確認-1")
                        #if OK:click(OK)
                    OK2=get_xy("OK3.png","確認-2")
                    if OK2:
                        OK2State=pyautogui.pixelMatchesColor(int(OK2.x),int(OK2.y),(254, 254, 254))
                        if OK2State:
                            click(OK2)
                        else:
                            OKColor=get_xy("item\\OKColor.png","確認顏色")
                            if OKColor:
                                ClickOK=pyautogui.pixelMatchesColor(int(OKColor.x),int(OKColor.y),(255, 193, 0))
                                click(OKColor)
                    
                    LevelUP=get_xy("Select\\LevelUP.png","加碼多多等級提升")
                    if LevelUP:click(LevelUP)
                    AutoNext+=1
                    if AutoNext>60:
                        click(CNext)
                        print("自動下一步")
                        AutoNext=0
                        time.sleep(3)
                    
                    
                AutoState=MoreSearch(listT=TestAddState,Name="加碼多多 尚未探險")
                if AutoState:
                    click(AutoState)
                    time.sleep(1)
                    
                    SetHour=1
                    if ItemGet.Play>0:
                        XPRange=ItemGet.Range().get('XP')
                        if XPRange>40:
                            SetHour=3
                        elif XPRange>70:
                            SetHour=6

                    BackCount+=SetHour
                    ItemGet.Hour+=SetHour
                    AutoA1=get_xy(f"Select\\{SetHour}HS.png",f"加碼多多{SetHour}H") 
                    if AutoA1:
                        time.sleep(1)
                        click(AutoA1)
                        time.sleep(3)
                        OK=get_xy("Select\\Yes.png","確定")
                        if OK:
                            Delay=10
                            click(OK)
                            ItemGet.Play+=1

                        time.sleep(3) #等待3秒

                        

                Gold=get_xy("Gold2.png","驗收")
                if Gold:
                    #兩次程式切換
                    click(Gold)
                    time.sleep(1)
                
                Next=get_xy("GetMore.png","下一步")
                if Next:
                    if Delay>=3:Delay=1
                    click(Next)
                GetM=get_xy("Get3.png","得到物品")    
                if GetM:
                    RG=(GetM.x-500,GetM.y-200,GetM.x+500,GetM.y+200)
                    FileRoot=f"ProjectPath\\Get\{CaptureF}.png"
                    pyautogui.screenshot(region=RG).save(FileRoot)
                    CaptureF+=1

                    Feed=get_xy('item/Feed.png',"獲得罐頭")
                    if Feed:
                        Feed1=get_xy('item/Feed/2.png',"獲得罐頭x2")
                        if Feed1:ItemGet.AddFeed(2)
                        else:   
                            ItemGet.AddFeed(1)
                        click(GetM)
                    
                    xp=get_xy('item/xp.png',"獲得xp")
                    if xp:
                        xp800=get_xy('item/xp/800.png',"獲得xp+800")
                        if xp800:
                            ItemGet.AddXP(800)
                        else:
                            ItemGet.AddXP(100)
                        click(GetM)

                    xp5k=get_xy('item/xp/5000.png',"獲得xp 5000")    
                    if xp5k:
                        ItemGet.AddXP(800)
                        click(GetM)

                    xp1w=get_xy('item/xp/10000.png',"獲得xp 10000")    
                    if xp1w:
                        ItemGet.AddXP(10000)
                        click(GetM)
                    xp3w=get_xy('item/xp/30000.png',"獲得xp 30000")    
                    if xp3w:
                        ItemGet.AddXP(3000)    
                    
                    

                Back=get_xy("Back.png","回來了")
                if Back:
                    click(Back,2)
                End=get_xy("End.png","探險結果")
                if End:
                    click(End,2)

                # GetItemU1=get_xy('item/ItemUP3.png',"道具提升隊員小")
                # GetMore2=get_xy("GetMore2.png","窗口存在")   
                # if GetItemU1:
                #     print("Yes")
                #     click(GetItemU1)       
                # if GetMore2:
                #     print('True')
                #GetReward=get_xy("Get.png","領取報酬")
                #if GetReward:
                #    click(GetReward,2)    
                #ItemGet.Rest=False
                AutoMode[2]=[pyautogui.position().x,pyautogui.position().y] #自動更新位置信息
            else:
                if Delay<120:
                    Delay+=1
                print("進入節能模式 頻率降低")
                with open('C:/Users/u01/Desktop/NuclearWeb/Status.txt', 'w') as f:
                    DictR=ItemGet.Range()
                    Range='探險數據不夠統計..'
                    if DictR:
                        Range=f"得到XP:{DictR.get('XP')}% 得到罐頭:{DictR.get('Feed')}%"

                    f.write(f"""
                    E1{ItemGet.ResultH()}E2
                    E3{Range}E4
                    """
                    )

    #else:
        #if Delay<5:Delay=5
        #print(f"非檢測中 檢測頻率調整為{Delay}")

    time.sleep(Delay)


