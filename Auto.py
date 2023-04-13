import pyautogui
import pydirectinput #用於點擊
from pynput import keyboard,mouse #鍵盤事件用
import time #等待用
import os #用來取當前文件位置
import cv2 #百分比調整
import random #隨機數

from CatFeed import *

#項目位置
ProjectPath=os.path.dirname(os.path.abspath(__file__))
print('Project >>',ProjectPath)

WebFile="C:/Users/u01/Desktop/NuclearWeb/Status.json"
"""用於指定任意位置存放統計結果"""

SearchWin="雷電模擬器"
"""
查找你需要的窗口
"""

Debug=3
"""
1 啟用測試模式(只監聽滑鼠鍵盤)

2 測試戰鬥AI Region位置 以及click功能Debug

3 不監聽滑鼠(為了避免斷點調試造成卡頓問題)
"""

Delay=3
"""
檢測延遲
"""
HourPlan=[]
HourList={
    'Count':[],
    'Map':[
        [1,1,1,3,3,3,6], #<40% xp
        [1,1,1,3,1,1,1], #40% xp
        [1,1,1,3,3,1,3] #70% xp
    ]
}
"""
實驗安排探險策略

設置一組1+1+1+3+3+6 小時組
Ex:[1,1,1,3,3,6] 把這組List存進Map裡即可

Map - [0] < 40% xp使用
    - [1] >= 40%以上
    - [2] >= 70%以上
"""

KeySet={
    'Exit':keyboard.Key.esc,
    'Auto':keyboard.KeyCode.from_char('c'),
    'Point':keyboard.KeyCode.from_char('h'),
    'TestResize':keyboard.KeyCode.from_char('v'),
    '-Delay':keyboard.KeyCode.from_char('-'),
    '+Delay':keyboard.KeyCode.from_char('+'),
    'AutoDelay':keyboard.KeyCode.from_vk(99),
    'WinRect':keyboard.KeyCode.from_char('m'),
    'HourList':keyboard.KeyCode.from_char('l')
    }
"""
按鍵快捷設定
"""

AutoMode=[0,[15,15],0,[10,10],0] 
""" 用於狀態確定/計數

[0]自動加碼多多狀態
[1]接替倒數

[1] -> [0]初始值 [1]默認刷新值

[2]戰鬥AI狀態
[3]自動下一步

[3] -> [0]初始值 [1]默認刷新值
(當初始值歸零是會更新值為默認值)

[4] 設定是否使用縮放比例

"""


AutoC=0

KeyCount={
    'ESC':[5,5],
    'Resize':[5,5]
}
"""
按鍵計數 - Dict

| 字典值 Dict | 說明 |
| --- | --- |
| ESC | 結束運行 |
| Resize | 測試重新縮放 |

| 按鍵列表值 | 說明  |
| --- | --- |
| 0 | 初始值 |
| 1 | 補充值 |
"""

Region=None #查找位置
CaptureF=0 #第幾張圖

HourCount=0

ItemGet=GetItem()

MSearchAddState=[
    '1.png', '2.png', '3.png', '4.png', '5.png', 
    '6.png', '7.png', '8.png', '9.png', '10.png',
    ]

os.system("title Auto加碼多多")


def RunCheck():
    print('未開發函式 - 待完善')

def HourGet(Maps=0,Debug=0):
    """"
    探險陣列
    
    Maps -- 選擇第幾組探險陣列

    Debug -- 1 開啟調試用信息

    Return -- List
        [0]取出這次探險幾小時

        [1]還有多少小時可以取(0時會補充)
    """
    global HourList
    HourValue=HourList.get('Count')
    
    if Debug==1:
        print(f"{HourList}:{HourValue} {type(HourValue)}")
        print(f"{len(HourValue)} 共 {sum(HourValue)} 小時")

    if len(HourValue)<=0:
        RevList=HourList.get("Map")[Maps]
        HourList["Count"]=RevList[::-1] #新反轉列表
        
        if Debug==1:print(f'策略Map已用盡 {HourList["Count"]} 使用第{Maps}組')
        return [1,sum(HourValue)]

    elif len(HourValue)>=1:
        POP=HourList["Count"].pop()
        print(f'LastElement:{POP}')
        return [POP,sum(HourValue)]
        
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

def click(xy,x1r=0,num=1,CDelay=0,Mode=0):
    """
    xy 位置
    x1r x偏易增減
    num 次數
    CDelay 間隔
    Mode 1 啟用點擊時 更新接替間隔()
    """
    for i in range(num):
        pydirectinput.mouseDown(xy[0]+x1r,xy[1])
        pydirectinput.mouseUp(xy[0]+x1r,xy[1]) 
        
        if CDelay==0:continue
        else:
            CDelay=random.randint(1,2)/10+CDelay
        
        time.sleep(CDelay)

    if Mode==1:
        if Mouselisten.is_alive():
            Mouselisten.stop()
            print("暫停滑鼠漸監聽")
        if Keylisten.is_alive():
            Keylisten.stop()
            print("暫停鍵盤監聽")

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
        Scale=WinTool.FWScale(Find_W=SearchWin,width=1920,height=1080)
        if Scale:
            CVScale=cv2Scale(img_path,[Scale[0],Scale[1]])
            Add=CVScale.get('imgFile')
    
    try:
        #檢測圖片
        if regionS:
            Position=pyautogui.locateCenterOnScreen(image=Add,confidence=confi,region=regionS)
        else:
            Position=pyautogui.locateCenterOnScreen(image=Add,confidence=confi)
    except Exception:
        print("User Control 使用者帳戶控制頁面不能進行截圖")
        return None

    if Position:
        print(f"{name} 找到了:{Position}")
        return Position
    elif tip==1:
        print(f"{name} 沒有")

def MoreSearch(dir="Add",listT=list(["1.png","2.png"]),Name="Test",Mode_=0,MDelay=0.5):
    """
    dir 設置所處資料夾
    listT ['1.png','2.png'] 多張查找列表
    Name 找到的名稱提示
    Mode_ 1 啟用動態縮放模式
    MDelay 查找間隔秒數
    """
    
    for i in listT:
        Num=listT.index(i)
        time.sleep(MDelay)
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
    global KeyCount,AutoMode

    if AutoMode[1][0]<=5:
        AutoMode[1][0]=AutoMode[1][1]
        if AutoMode[0]==1:AutoMode[0]=0

    elif str(key)==str(KeySet.get("AutoDelay")):
        if AutoMode[1][0]>1:
            AutoMode[1][0]-=1
            print(f"降低接替間隔:{AutoMode[1][0]}")


    if key == KeySet.get('Exit'):
            print(f"再按{KeyCount.get('ESC')[0]}次 結束")
            KeyCount['ESC'][0]-=1
            if KeyCount.get('ESC')[0]<=0:
                print(ItemGet.Result())
                print('結束進程')
                os._exit(0)
    else:
        KeyCount['ESC'][0]=KeyCount['ESC'][1] #補充值
    
        if key == KeySet.get('Auto'):
            if AutoMode[2]==0:
                AutoMode[2]=1
                print("啟用自動戰鬥簡易操作")
            else:
                AutoMode[2]=0
                print("關閉自動戰鬥")
        elif key == KeySet.get('Point'):
            print(pyautogui.position())    
    
    
        if key == KeySet.get('TestResize'):
                print(f"再按{KeyCount.get('Resize')[0]}次 運行")
                KeyCount["Resize"][0]-=1
                
                if KeyCount["Resize"][0]<=0:
                    global ProjectPath,SearchWin
                    print("正在運行Resize結果")  

                    ScaleFW=WinTool.FWScale(Find_W=SearchWin,width=1280,height=720,tip=1)
                    ReSize=cv2Scale('Add_5.png',scale_percent=[ScaleFW[0],ScaleFW[1]],Debug=True,ReadF=True)
                    print(f"imgFile:{ReSize.get('imgFile')}")
                    FRWW=get_xy(img_path=ReSize.get('imgFile'),name=">> 測試Resize",tip=1)
                    if FRWW:
                        #計算擷取範圍
                        print(FRWW)
                        REG=((FRWW.x-FRWW.x*0.1),(FRWW.y-FRWW.y*0.1),(FRWW.x+FRWW.x*0.1),(FRWW.y+FRWW.y*0.1))
                        pyautogui.screenshot(region=REG).save(f'{ProjectPath}\\Test\\ResizeR.png')
                        cv2Tool.ShowImage(f"{ProjectPath}\\Test\\ResizeR.png","FindResult")
                        
                    cv2Tool.ShowImage(ReSize.get('img'),"Resize")
                    
                    KeyCount["Resize"][0]=KeyCount["Resize"][1]
                
        else:
            KeyCount["Resize"][0]=KeyCount["Resize"][1]

        global Delay
        if key == KeySet.get("-Delay"):
            print(f"降低延遲間隔:{Delay}")
            if Delay>1:Delay=round(Delay-1)
            elif Delay>=0.2:Delay=round(Delay-0.1,1)

        elif key == KeySet.get("+Delay"):
            print(f"增加延遲間隔:{Delay}")
            if Delay<1:Delay=round(Delay+0.1,1)
            else:Delay=round(Delay+1)
        
        elif key == KeySet.get("WinRect"):
            FWinD=WinTool.FindW(Window=SearchWin)
            if FWinD:
                print(FWinD[2])

        elif key == KeySet.get('HourList'):
            HGet=HourGet(Debug=1 ,Maps=2)
            print(f">> 這次探險{HGet[0]}時 還可以取{HGet[1]}時")
        elif key == keyboard.KeyCode.from_char("p"):
            print("測試click Mode 1")
            xy=pyautogui.position()
            click(xy,Mode=1)
    

MoveTest=True
#滑鼠
def move(x,y):
    global MoveE,MoveTest

    if MoveTest:
        if len(MoveE)<2:
            MoveE.append({'x':x,'y':y})
        elif len(MoveE)>=2:
            global Distances
            distance = WinTool.get_distance(MoveE[0], MoveE[1])
            Distances.append(distance)
            if len(Distances)>=30:
                DisSum=sum(Distances)

                global Debug

                RRAND=random.randrange(10,25)

                if Debug==1:
                    print(f'30次偏差和:{DisSum}')
                    print(f"將重新取得{RRAND}個元素")
                
                if DisSum>=330:
                    global AutoMode
                    
                    if AutoMode[1][0]<=5:
                        AutoMode[1][0]=AutoMode[1][1]
                        if AutoMode[0]==1:AutoMode[0]=0
                        if Debug==1:print(f"刷新值[滑鼠移動]:{AutoMode[1][0]}")
                
                
                for i in range(RRAND):
                    Distances.pop()
            MoveE.clear()
    else:
        print("停用滑鼠移動檢測")

def mclick(k1,k2,k3,k4):
    """
    k1&k2 - 滑鼠x,y位置

    k3 - 按下按鍵

    k4 - 是否正按下 
    """
    global Debug,MoveTest
    
    if Debug==1:
        print((k1,k2),k3,k4,type(k4))
    if MoveTest:
        if k4:
            global AutoMode
            if AutoMode[1][0]<=5:
                AutoMode[1][0]=AutoMode[1][1]
                if AutoMode[0]==1:AutoMode[0]=0

                if Debug==1:print(f"刷新值[滑鼠點擊]:{AutoMode[1][0]}")
    else:
        print("停用滑鼠點擊檢測")

#鍵盤按鍵接收
Keylisten=keyboard.Listener(on_press=press)
Keylisten.start()
#滑鼠移動檢測
Mouselisten=mouse.Listener(on_move=move, on_click=mclick)
if Debug!=3: #如果再調試其他部分 建議先不要監聽滑鼠活動
    Mouselisten.start()
else:
    print("不調試滑鼠!")

ListenResume=[10,10]




while True:
    Position=pyautogui.position()
    DictText={
        "Position":Position,
        "Delay":Delay,
        "AutoMode":AutoMode,
        "MListen":Mouselisten.is_alive(),
        "KListen":Keylisten.is_alive(),
        "Time":WinTool.NowTime()
    }
    DisplayText=[
        "當前位置:{Position} 延遲:{Delay} 狀態:{AutoMode[0]}",
        "自動下一步{AutoMode[3]} 接替於:{AutoMode[1][0]}",
        "M:{MListen} Key:{KListen}",
        "-- {Time}"
    ]
    DisplayText.insert(0,"="*len(DisplayText[0]))
    DisplayText.append("="*len(DisplayText[0]))
    print("\n".join(DisplayText).format_map(DictText))
    #LDOperationRecorderWindow 操作錄製窗口
    #LDPlayerMainFrame 主窗口    
    
    if Debug==1:
        print(f"只測試鍵盤滑鼠")
        time.sleep(Delay)
        continue
    
    if not Keylisten.is_alive() or not Mouselisten.is_alive():
        print(f"鍵盤/滑鼠 監聽於:{ListenResume[0]}秒後啟用")
        ListenResume[0]-=Delay
    if ListenResume[0]<1:
        ListenResume[0]=ListenResume[1]
        #建立新的監聽
        if not Keylisten.is_alive():
            Keylisten=keyboard.Listener(on_press=press)
            Keylisten.start()
        elif not Mouselisten.is_alive():    
            if Debug==3:
                print(f"調試模式:{Debug} 不啟用滑鼠")
                continue
            Mouselisten=mouse.Listener(on_move=move, on_click=mclick)
            Mouselisten.start()


    if AutoMode[1][0]<=0:
        AutoMode[0]=1
        AutoMode[1][0]=AutoMode[1][1]
        
    else:AutoMode[1][0]-=1
    
    
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
                cv2Tool.ShowImage(f'{ProjectPath}\\Test\RCat.png','測試範圍')


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


    elif AutoMode[0]==1:
        if Delay>3:
            Delay-=1
        
        Work1=get_xy("Work.png","加碼多多 正在探險",Mode=1)
        if Work1 == None: #非探險
            

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
            
            CNext=get_xy("Select\\NextCheck.png","可下一步",Mode=1)
            if CNext:
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
                if LevelUP:click(LevelUP,Mode=1)
                
                if AutoMode[3][0]>0:AutoMode[3][0]-=1
                elif AutoMode[3][0]<=0:
                    click(CNext,Mode=1)
                    print("自動下一步")
                    AutoMode[3][0]=AutoMode[3][1]
                    time.sleep(3)
                
                
            AutoState=MoreSearch(listT=MSearchAddState,Name="加碼多多 尚未探險",Mode_=1)
            if AutoState:
                click(AutoState)
                time.sleep(3)
                
                MapsS=0 #第幾組Map
                if ItemGet.Play<40:
                    XPRange=ItemGet.Range().get('XP')
                    if XPRange>=40:
                        MapsS=1
                    elif XPRange>=70:
                        MapsS=2
                SetHour=HourGet(Maps=MapsS,Debug=1)[0]
                
                HourPlan.append(SetHour) #紀錄使用策略

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
                    WinRect=SWW[2]
                    with open(f"{ProjectPath}\\Get\\Screen.txt", "a") as f:
                        f.write(f"[{WinTool.NowTime()}]\n窗口區域:{CaptureF}:{WinRect}\n")
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
                    ItemGet.AddXP(5000,Type_D='5KCount')
                    click(GetM,Mode=1)

                xp1w=get_xy('item/xp/10000.png',"獲得xp 10000",Mode=1)    
                if xp1w:
                    ItemGet.AddXP(10000)
                    click(GetM,Mode=1)
                xp3w=get_xy('item/xp/30000.png',"獲得xp 30000",Mode=1)    
                if xp3w:
                    ItemGet.AddXP(30000,Type_D='3WCount')    
                xp5w=get_xy('item/xp/50000.png',"獲得xp 50000",Mode=1)    
                if xp5w:
                    ItemGet.AddXP(50000,Type_D='5WCount')    
                

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
            if Delay<60:
                Delay+=1
            print("進入節能模式 頻率降低")

            #用於更新網站根目錄特定檔案的內容
            if WebFile:
                RString=""
                AP=0
                for i in HourPlan:
                    if AP<=3:
                        Add='+'
                        if AP>=3:
                            Add='\n'
                            AP=0
                        RString=f"{RString}{i}"+ Add 

                    AP+=1
                
                
                import json

                DictR=ItemGet.Range()
                Range='探險數據不夠統計..'
                if DictR:
                    Range=f"得到XP:{DictR.get('XP')}% 得到罐頭:{DictR.get('Feed')}%"

                ResultRS={
                    "Result":ItemGet.ResultH(),
                    "RSCount":Range,
                    "HourPlan":RString
                }
                with open(WebFile, 'w',encoding='utf-8') as f:
                    json.dump(ResultRS,f,indent=4,ensure_ascii=False)
                    #寫入檔案以json格式


    time.sleep(Delay)


