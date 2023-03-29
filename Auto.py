import pyautogui
import pydirectinput #用於點擊
from pynput import keyboard,mouse #鍵盤事件用
import time #等待用
import os #用來取當前文件位置
import win32gui #窗口范範圍捕抓
import cv2 #百分比調整
import random #隨機數
import threading
from CatFeed import *

#項目位置
ProjectPath=os.path.dirname(os.path.abspath(__file__))
print('Project >>',ProjectPath)

WebFile="C:/Users/u01/Desktop/NuclearWeb/Status.txt" #用於指定任意位置存放統計結果
SearchWin="雷電模擬器" #查找你需要的窗口

Debug=0
#1 啟用測試模式(只監聽滑鼠鍵盤)
#2 測試戰鬥AI Region位置 以及click功能Debug

Delay=3 #檢測延遲

KeySet={
    'Exit':keyboard.Key.esc,
    'Auto':keyboard.KeyCode.from_char('c'),
    'Point':keyboard.KeyCode.from_char('h'),
    'TestResize':keyboard.KeyCode.from_char('v'),
    '-Delay':keyboard.KeyCode.from_char('-'),
    '+Delay':keyboard.KeyCode.from_char('+'),
    'AutoDelay':keyboard.KeyCode.from_vk(99),
    'WinRect':keyboard.KeyCode.from_char('m')
    }

AutoMode=[0,15,0,30,4] #用於確定是否需要自動接替
# [0]自動加碼多多狀態
# [1]接替倒數
# [2]戰鬥AI狀態
# [3]自動下一步
# [4] 設定是否使用縮放比例

AutoC=0

ESCCount=0 #退出按鍵計數
Region=None #查找位置
CaptureF=0 #第幾張圖

HourCount=0

ItemGet=GetItem()

MSearchAddState=[
    '1.png', '2.png', '3.png', '4.png', '5.png', 
    '6.png', '7.png', '8.png', '9.png', '10.png',
    ]

os.system("title Auto加碼多多")


def FWScale(Find_W='雷電模擬器',width=1920,height=1080,tip=0):
    """FWScale 用於計算縮放百分比

    Keyword Arguments:
        Find_W -- 查找指定窗口 (default: {'雷電模擬器'})
        width -- 原始圖片分辨率 (default: {1920})
        height -- 原始圖片分辨率 (default: {1080})

        原始圖片分辨率是 指在原始窗口最大寬高下進行擷取的分辨率

        tip -- 1 啟用偵錯信息 (default: {0})

    Returns:
        [0.3,0.1] 寬百分比 & 高百分比
    """
    FWinD=WinTool.FindW(Window=Find_W)
    if FWinD:
        WH=win32gui.GetWindowRect(FWinD[2]) #取得窗口範圍
        widthW=WH[2]-WH[0]
        heightH=WH[3]-WH[1]

        if tip==1:print(WH,widthW,heightH)
        ScaleW=round(widthW/width,2)
        ScaleH=round(heightH/height,2)
        if tip==1:print(ScaleW,ScaleH)

        return [ScaleW,ScaleH]
    
def cv2Scale(image,scale_percent=[0.8,0.3],Debug=False,ReadF=False):
    """cv2Scale 用於重新縮放圖片

    Arguments:
        image -- 圖片路徑(img資料夾下)

    Keyword Arguments:
        scale_percent -- 縮放百分比 (default: [0.8,0.3])
        [0]:調整寬度百分比 0代表不調整
        [1]:調整高度百分比 0代表不調整

        Debug -- True (default:False) 啟用偵錯用信息
        ReadF -- True (default:False) 啟用img回傳(給cv2.imread預覽用)
    Returns:
        調整後的圖片[字典] imgFile:新圖片路徑 img:用於cv2.imread預覽用
    """
    imgRF=os.path.join(ProjectPath,"img",image) #原始圖片路徑
    imgRF2=os.path.dirname(imgRF) #上層資料夾(檔案的上一層)
    imgRF3=os.path.abspath(os.path.join(imgRF2,'..')) #上層資料夾

    imgFName=os.path.basename(image)
    
    if Debug:print(f"""
    1:{imgRF}
    2:{imgRF2}
    3:{imgRF3}
    File:{imgFName}
    Scale:{scale_percent}
    """)
    
    File_Root=f"{imgRF2}\\Resize" #縮放調整指定資料夾
    Image_Root=f"{File_Root}\\{imgFName}" #縮放指定資料夾下的圖片

    #結果回傳
    Result={
        'imgFile':Image_Root,
        'img':None,
    }
    
    img=cv2.imread(imgRF,cv2.IMREAD_UNCHANGED) #原始圖片樣本讀取
    
    width,height = int(img.shape[1]),int(img.shape[0]) #原始寬高讀取
    
    if Debug:print(f"原始:{width},{height}")

    if scale_percent[0]!=0:
        width=int(width*scale_percent[0]) #縮放比例寬計算
    if scale_percent[1]!=0:
        height=int(height*scale_percent[1]) #縮放比例高計算

    if Debug:print(f"原始調整後:{width},{height}")

    #如果縮放資料夾下存在調整過的圖片
    if os.path.exists(Image_Root):
        ResizeImg=cv2.imread(Image_Root,cv2.IMREAD_UNCHANGED) #已處理過的圖片
        RWidth,RHeight=int(ResizeImg.shape[1]),int(ResizeImg.shape[0]) #已處理寬高讀取
        
        RWWi=[RWidth-width,RHeight-height] #用於方便判斷是否放大還是縮小
        if RWWi[0]<0:RWWi[0]=width-RWidth #反向寬縮放計算
        if RWWi[1]<0:RWWi[1]=height-RHeight #反向高縮放計算

        if Debug:print(f"""
                已經有調整過的樣本了!
                R:{RWidth} {RHeight} N:{width} {height}
                RWWi:{RWWi}
            """
            )
        
        if RWWi[0]<30 and RWWi[1]<30:
            if Debug:print(f"寬高差異在30相素以內")
            
            if ReadF:Result["img"]=ResizeImg
            return Result

    if Debug:print(f"樣本差異大於30需調整")

    resizeR=cv2.resize(img, (width,height)) #重新調整圖片

    if Debug:print(f"{File_Root}")
    
    if not os.path.exists(File_Root):
        os.makedirs(File_Root)
        cv2.imwrite(Image_Root,resizeR)
    else:
        if Debug:print("已經存在Resize資料夾了呦!")
        cv2.imwrite(Image_Root,resizeR)

    if ReadF:Result["img"]=resizeR
    return Result

def click(xy,x1r=0,num=1,Delay=0,Mode=0):
    """
    xy 位置
    x1r x偏易增減
    num 次數
    Delay 間隔
    Mode 1 啟用點擊時 更新接替間隔()
    """
    for i in range(num):
        pydirectinput.mouseDown(xy[0]+x1r,xy[1])
        pydirectinput.mouseUp(xy[0]+x1r,xy[1]) 
        
        if Delay==0:continue
        else:
            Delay=random.randint(1,2)/10+Delay
        
        time.sleep(Delay)

    if Mode==1:
        global AutoMode,Debug
        if AutoMode[1]>3:AutoMode[1]=3
        if Debug==2:print(f"自動點擊間隔更新! {AutoMode[1]}")
        #避面自動點擊 誤判使用者活動

def get_xy(img_path=None,name="測試",tip=None,confi=0.9,regionS=None,Mode=0):
    """
    img_path 檢測圖片位置\n
    name 顯示名稱\n
    tip 提示沒有找到 1開啟 預設關閉\n
    confi 相似度\n
    regionS 擷取範圍
    Mode 1使用新Resize百分比調整
    """
    if img_path is None:return '沒有指定圖片'

    Add=os.path.join(ProjectPath,"img",img_path) #用於圖片查找位置存放

    if Mode==1:
        Scale=FWScale(Find_W=SearchWin,width=1920,height=1080)
        if Scale:
            CVScale=cv2Scale(img_path,[Scale[0],Scale[1]])
            Add=CVScale.get('imgFile')
    
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

def ShowImage(img=None,title="TestShowImg",Delay=5000):
    """ShowImage 顯示圖片

    Keyword Arguments:
        img -- 指定圖片位置 (default: {None})
        title -- 顯示窗口名稱 (default: "TestShowImg") 
        Delay -- 設定圖片展示幾秒後關閉 (default: {5000})
    """
    if img is None:
        print("沒有圖片輸入!")
        return
        
    WinTool.Thread(
        lambda:( #用於快捷定義func運行多個命令
            cv2.imshow(title,img),
            cv2.waitKey(Delay),
            cv2.destroyAllWindows()
        )
    )

def MoreSearch(dir="Add",listT=list(["1.png","2.png"]),Name="Test",Mode_=0,Delay=0.5):
    """
    dir 設置所處資料夾
    listT ['1.png','2.png'] 多張查找列表
    Name 找到的名稱提示
    Mode_ 1 啟用動態縮放模式
    Delay 查找間隔秒數
    """
    
    for i in listT:
        Num=listT.index(i)
        time.sleep(Delay)
        FindListT=get_xy(f"{dir}\\{listT[Num]}",Name,Mode=Mode_)
        if FindListT:
            return FindListT
        else:
            return None
        

MoveE=[]
Distances=[]

#鍵盤
def press(key):
    """
    key 接收按下的按鍵
    鍵盤按鍵接收用
    """
    global ESCCount,AutoMode,Delay,SearchWin,ProjectPath
    
    #print(key,type(key))
    if AutoMode[0]==1:
        AutoMode[0]=0
        
    if key == KeySet.get('Exit'):
            ESCCount+=1
            if ESCCount>=5:
                print(ItemGet.Result())
                print('結束進程')
                os._exit(0)
    elif key == KeySet.get('Auto'):
        if AutoMode[2]==0:
            AutoMode[2]=1
            print("啟用自動戰鬥簡易操作")
        else:
            AutoMode[2]=0
            print("關閉自動戰鬥")
    elif key == KeySet.get('Point'):
        print(pyautogui.position())    
    
    elif key == KeySet.get('TestResize'):
        ScaleFW=FWScale(Find_W=SearchWin,width=1280,height=720,tip=1)
        ReSize=cv2Scale('Add_5.png',scale_percent=[ScaleFW[0],ScaleFW[1]],Debug=True,ReadF=True)
        print(f"imgFile:{ReSize.get('imgFile')}")
        FRWW=get_xy(img_path=ReSize.get('imgFile'),name=">> 測試Resize",tip=1)
        if FRWW:
            #計算擷取範圍
            print(FRWW)
            REG=((FRWW.x-FRWW.x*0.1),(FRWW.y-FRWW.y*0.1),(FRWW.x+FRWW.x*0.1),(FRWW.y+FRWW.y*0.1))
            pyautogui.screenshot(region=REG).save(f'{ProjectPath}\\Test\\ResizeR.png')
            ShowImage(f"{ProjectPath}\\Test\\ResizeR.png","FindResult")
            
        ShowImage(ReSize.get('img'),"Resize")

    elif key == KeySet.get("-Delay"):
        print(f"降低延遲間隔:{Delay}")
        if Delay>1:Delay=round(Delay-1)
        elif Delay>=0.2:Delay=round(Delay-0.1,1)

    elif key == KeySet.get("+Delay"):
        print(f"增加延遲間隔:{Delay}")
        if Delay<1:Delay=round(Delay+0.1,1)
        else:Delay=round(Delay+1)
        
    
    elif str(key)==str(KeySet.get("AutoDelay")):
        if AutoMode[1]>1:
            AutoMode[1]-=1
            print(f"降低接替間隔:{AutoMode[1]}")
        
    elif key == KeySet.get("WinRect"):
        FWinD=WinTool.FindW(Window=SearchWin)
        if FWinD:
            WH=win32gui.GetWindowRect(FWinD[2])
            print(WH)
#滑鼠
def move(x,y):
    global AutoMode,MoveE,Distances,Debug
    if len(MoveE)<2:
        MoveE.append({'x':x,'y':y})
    if len(MoveE)==2:
        distance = round(WinTool.get_distance(MoveE[0], MoveE[1]))
        Distances.append(distance)
        
        if len(Distances)==30:
            DisSum=sum(Distances)
            if Debug==1:print(f'10次偏差和:{DisSum}')
            
            if DisSum>300:
                if AutoMode[0]==1:
                    AutoMode[0]=0
                elif AutoMode[1]<15:
                    AutoMode[1]=15
            
            Distances.clear()
        MoveE.clear()


#鍵盤按鍵接收
listen=keyboard.Listener(on_press=press)
listen.start()
#滑鼠移動檢測
listen2=mouse.Listener(on_move=move)
listen2.start()


while True:
    if ESCCount>0:ESCCount-=1
    Position=pyautogui.position()
    print(f"""
    當前位置:{Position} 延遲:{Delay} 狀態:{AutoMode[0]}
    自動下一步:{AutoMode[3]} 接替於:{AutoMode[1]} ESC:{ESCCount}
    """)
    #LDOperationRecorderWindow 操作錄製窗口
    #LDPlayerMainFrame 主窗口    
    
    if Debug==1:
        print(f"只測試鍵盤滑鼠")
        time.sleep(Delay)
        continue
    
    if AutoMode[1]<=0:
        AutoMode[0]=1
        AutoMode[1]=5
        
    if AutoMode[1]>0:AutoMode[1]-=1
    
    
    HasRun=get_xy('HasRun.png',"正在遊戲中")    
    if HasRun and AutoMode[2]==1:
        Shot=get_xy("Play\\Shot3.png","貓咪炮")
        
        if Shot:
            Region=((HasRun.x-round(HasRun.x*0.6)),Shot.y-round(Shot.y*0.23),(Shot.x+round(Shot.x*0.005)),round(Shot.y*0.35))
            
            #測試擷取位置
            if Debug==2:
                print(Region,Shot)
                SE=pyautogui.screenshot(region=Region)
                SE.save(f'{ProjectPath}\\Test\\RCat.png')
                ShowImage(f'{ProjectPath}\\Test\RCat.png','測試範圍')


        if Region!=None:
            # Squirrel=get_xy('Play\\AT\\BSquirrel.png',"黑松鼠")
            BlackCat=get_xy('Play\\AT\\BlackCat.png',"黑熊")

            if BlackCat:
                if Shot:keyboard.Events.Press('2')

            #'Cat':[get_xy('Play\\Wall.png',"基本牆"),None,75]
            # [0] 查找對象 [1] 可出擊顏色 [2] 價錢
            Cannon_Fodder={
                'Cat':[get_xy('Play\\Cat.png',"小貓",regionS=Region),(151, 151, 148),75],
                'BigCat':[get_xy('Play\\BigCat.png',"大狂小貓",regionS=Region),(153, 154, 156),75]
            }
            for i in Cannon_Fodder:
                Cannon=Cannon_Fodder[i]
                if Cannon[0]:
                    CatX,CatY=int(Cannon[0].x),int(Cannon[0].y)
                    print(f"{i}:{pyautogui.pixel(CatX,CatY)}") #確認顏色

                    MatchColor=pyautogui.pixelMatchesColor(CatX,CatY,Cannon[1])
                    print(f"{i} 可出擊:{MatchColor}")
                    if MatchColor:
                        click(Cannon[0])
            
            if AutoC>=1:
                Wall={
                    'Wall':[get_xy('Play\\Wall.png',"基本牆",regionS=Region),(255, 255, 255),150],
                    'BigWall':[get_xy('Play\\BigWall.png',"大狂牆",regionS=Region),(255, 255, 255)],
                    'JumpCat':[get_xy('Play\\JumpCat.png',"跳跳貓",regionS=Region),(67, 46, 0)]
                }
                for i in Wall:
                    Wall_W=Wall[i]
                    if Wall_W[0]:
                        CatX,CatY=int(Wall_W[0].x),int(Wall_W[0].y)

                        print(f"{i}:{pyautogui.pixel(CatX,CatY)}") #確認顏色

                        MatchColor=pyautogui.pixelMatchesColor(CatX,CatY,Wall_W[1])
                        print(f"{i} 可出擊:{MatchColor}")
                        if MatchColor:
                            click(Wall_W[0])            
            
            if AutoC>=10:
                SuperCat={
                    'RamenCat':[get_xy('Play\\RamenCat.png',"拉麵貓",regionS=Region),(83, 61, 11)],
                    'BigBird':[get_xy('Play\\BigBird.png',"大狂鳥",regionS=Region),(153, 124, 54)],
                    'FlyingCat':[get_xy('Play\\FlyingCat.png',"飛腳貓",regionS=Region),(79, 52, 2)],
                    'Mutt38':[get_xy('Play\\Mutt38.png',"姆特",regionS=Region),(229, 198, 127)]
                }
                for i in SuperCat:
                    SuCat=SuperCat[i]

                    if SuCat[0]:
                        CatX,CatY=int(SuCat[0].x),int(SuCat[0].y)
                        
                        print(f"{i}:{pyautogui.pixel(CatX,CatY)}") #確認顏色
                        
                        if SuCat[1]==None:continue #沒有指定顏色先跳過
                        MatchColor=pyautogui.pixelMatchesColor(CatX,CatY,SuCat[1])
                        print(f"{i} 可出擊:{MatchColor}")
                        if MatchColor:
                            click(SuCat[0])
                time.sleep(2)
                AutoC=0
            print(f'AutoC:{AutoC}')
            AutoC+=Delay #動態出貓間隔


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
            
            Work1=get_xy("Work.png","加碼多多 正在探險",Mode=1)
            if Work1 == None: #非探險
                CNext=get_xy("Select\\NextCheck.png","可下一步",Mode=1)

                SelectS=get_xy("SelectS.png","選項界面",Mode=1)
                if SelectS==None:
                    Cancel=get_xy("Cancel.png","關閉頁面",Mode=1)
                    if Cancel:
                        click(Cancel)

                Base=get_xy("Base.png","正在基地",Mode=1)
                if Base:
                    Addd=get_xy("Add4.png","去加碼多多",Mode=1)
                    if Addd:
                        click(Addd)
                

                if CNext:
                    Delay=1
                    Card=get_xy("item\\Card.png","獲得貓咪卷")
                    if Card:
                        time.sleep(1)
                        OK=get_xy("OK3.png","確認-1")
                        if OK:click(OK)
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
                    
                    LevelUP=get_xy("Select\\LevelUP.png","加碼多多等級提升",Mode=1)
                    if LevelUP:click(LevelUP)
                    
                    if AutoMode[3]>0:AutoMode[3]-=1
                    if AutoMode[3]==0:
                        click(CNext)
                        print("自動下一步")
                        AutoMode[3]=30
                        time.sleep(3)
                    
                    
                AutoState=MoreSearch(listT=MSearchAddState,Name="加碼多多 尚未探險",Mode_=1)
                if AutoState:
                    click(AutoState)
                    time.sleep(3)
                    
                    SetHour=1
                    if ItemGet.Play>0:
                        XPRange=ItemGet.Range().get('XP')
                        if XPRange>40:
                            SetHour=3
                        elif XPRange>70:
                            SetHour=6

                    HourCount+=SetHour
                    ItemGet.Hour+=SetHour
                    AutoA1=get_xy(f"Select\\{SetHour}HS.png",f"加碼多多{SetHour}H",Mode=1) 
                    if AutoA1:
                        time.sleep(3)
                        click(AutoA1,Mode=1)
                        time.sleep(3)
                        OK=get_xy("Select\\Yes.png","確定",Mode=1)
                        if OK:
                            Delay=10
                            click(OK,Mode=1)
                            ItemGet.Play+=1

                        time.sleep(3) #等待3秒

                        

                Gold=get_xy("Gold.png","驗收",Mode=1)
                if Gold:
                    click(Gold,Mode=1)
                
                Next=get_xy("Select\\Next.png","下一步",Mode=1)
                if Next:
                    if Delay>=3:Delay=1
                    click(Next,Mode=1)
                GetM=get_xy("Get3.png","得到物品",Mode=1)    
                if GetM:
                    RG=(GetM.x-700,GetM.y-400,GetM.x+500,GetM.y+100)
                    
                    CheckFile=None #檢測是否相似用
                    FileRoot=f"{ProjectPath}\\Get\{CaptureF}.png"
                    
                    while os.path.exists(FileRoot): #已存在檔案檢測
                        print(f'{FileRoot}:存在')
                        
                        CheckFile=get_xy(FileRoot,'檢測是否此檔案相似')
                        CaptureF+=1
                        FileRoot=f"{ProjectPath}\\Get\{CaptureF}.png"
                    
                    if CheckFile is None:
                        pyautogui.screenshot(region=RG).save(FileRoot)
                    else:
                        print("截圖相符! 已略過新存儲")

                    SWW=WinTool.FindW(Window=SearchWin)
                    if SWW:
                        print("已找到窗口")
                        WinRect=win32gui.GetWindowRect(SWW[2])
                        with open(f"{ProjectPath}\\Get\\Screen.txt", "a") as f:
                            f.write(f"[{WinTool.NowTime}]\n窗口區域:{CaptureF}:{WinRect}\n")
                    else:
                        print(f"沒找到窗口{SWW}")
                        

                    Feed=get_xy('item/Feed.png',"獲得罐頭",Mode=1)
                    if Feed:
                        Feed1=get_xy('item/Feed/2.png',"獲得罐頭x2",Mode=1)
                        if Feed1:ItemGet.AddFeed(2)
                        else:   
                            ItemGet.AddFeed(1)
                        click(GetM,Mode=1)
                    
                    xp=get_xy('item/xp.png',"獲得xp",Mode=1)
                    if xp:
                        xp800=get_xy('item/xp/800.png',"獲得xp+800",Mode=1)
                        if xp800:
                            ItemGet.AddXP(800)
                        else:
                            ItemGet.AddXP(100)
                        click(GetM,Mode=1)

                    xp5k=get_xy('item/xp/5000.png',"獲得xp 5000",Mode=1)    
                    if xp5k:
                        ItemGet.AddXP(800)
                        click(GetM,Mode=1)

                    xp1w=get_xy('item/xp/10000.png',"獲得xp 10000",Mode=1)    
                    if xp1w:
                        ItemGet.AddXP(10000)
                        click(GetM,Mode=1)
                    xp3w=get_xy('item/xp/30000.png',"獲得xp 30000",Mode=1)    
                    if xp3w:
                        ItemGet.AddXP(3000)    
                    
                    

                Back=get_xy("Back.png","回來了",Mode=1)
                if Back:
                    click(Back,Mode=1)
                End=get_xy("End.png","探險結果",Mode=1)
                if End:
                    click(End,Mode=1)

                if HourCount>=6:
                    HourCount=0
                    BackBaseC=get_xy("Back2.png","每6小時 返回驗收確認",Mode=1)
                    if BackBaseC:click(BackBaseC)
                
            else:
                if Delay<120:
                    Delay+=1
                print("進入節能模式 頻率降低")

                #用於更新網站根目錄特定檔案的內容
                if WebFile:
                    with open(WebFile, 'w') as f:
                        DictR=ItemGet.Range()
                        Range='探險數據不夠統計..'
                        if DictR:
                            Range=f"得到XP:{DictR.get('XP')}% 得到罐頭:{DictR.get('Feed')}%"

                        f.write(f"""
                        E1{ItemGet.ResultH()}E2
                        E3{Range}E4
                        """
                        )


    time.sleep(Delay)


