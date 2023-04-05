"""
用於統計得到物品用
"""
import time,math
import threading
import win32gui

class WinTool:
    """
    一些工具函式
    """
    def get_distance(point1, point2):
        """get_distance 計算兩點偏差值

        Arguments:
            point1 -- Dict{'x':30,'y':30}
            point2 -- Dict{'x':30,'y':30}

        Returns:
            偏差值
        """
        x1, y1 = point1['x'], point1['y']
        x2, y2 = point2['x'], point2['y']
        return round(math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2))

    def Thread(func,argsR=None,Mode=0):
        """Thread 運行新線程

        會運行func的內容

        Arguments:
            func -- 指定觸發函式
            argsR -- 傳遞給指定函式的參數
            Mode -- 1 加入線程列表
        """
        if argsR:
            T1=threading.Thread(target=func,args=argsR)
        else:T1 = threading.Thread(target=func)
        
        #print(T1.getName(),T1.is_alive())
        if Mode==0:
            T1.start()
        else:
            T1.start()
            T1.join()

    def FindW(Class=None,Window=None):
        """
        用於指定窗口定位

        Window 查找特定窗口名稱
        Class 纇名

        Return -- list
            [0]:ClassName
            [1]:WindowText
            [2]:WindowRect
            [3]:handle

        """
        handle=win32gui.FindWindow(Class,Window)
        if handle == 0:
            return None
        else:
            temp=[
                win32gui.GetClassName(handle),
                win32gui.GetWindowText(handle),
                win32gui.GetWindowRect(handle),
                handle,
            ]
            return temp
    
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
        FWinD=__class__.FindW(Window=Find_W)
        if FWinD:
            WH=FWinD[2] #取得窗口範圍
            widthW,heightH=WH[2]-WH[0],WH[3]-WH[1]

            if tip==1:print(WH,widthW,heightH)
            ScaleW,ScaleH=round(widthW/width,2),round(heightH/height,2)
            if tip==1:print(ScaleW,ScaleH)

            return [ScaleW,ScaleH]
    
    def WCall(handle,extra):
        """
        WCall - 獲取窗口標題並打印
        
        handle 句柄
        extra 格式設定
        """
        wind=extra
        temp=[]
        temp.append(win32gui.GetWindowText(handle))
        wind[handle]=temp
        print(f"{handle}:{extra}")


    def CheckActiveWindow():
        """
        此方法獲取正在使用窗口信息

        return 字典 Dict 
            窗口標題 Text 標題長度 Len

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



    def NowTime(Format=f"%Y/%m/%d %p %H:%M:%S",**Replace):
        """
        Format:f"%Y/%m/%d" 顯示樣式調整
        
        Replace:文字替換
        使用方法:設定一個你要替換的參數

        例:NowTime(AM="上午")
            字串結果裡會找到替換AM成上午

        例2:NowTime(_2023=2023年)
            如果你要用數字只要前面先加上_即可

            會取_後的文字

        Return:String 本地時間
        """
        curTime=time.time()
        format_time=time.localtime(curTime) #本地時間
        
        str=time.strftime(Format,format_time) #格式轉換
        
        for key in Replace:
            if key.find("_") != -1:
                keyS=key.split("_")[1]
            else:
                keyS=key

            str = str.replace(keyS, Replace[key])
        
        return str
    


import cv2
class cv2Tool:
    """
    此類整合了 關於使用cv2方法
    """
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
            ),Mode=1
        )

    def Search(img1,imgF,ORB=cv2.SIFT.create(1000),matcher=cv2.BFMatcher(),confi=0.7):
        """Search 使用SIFT算法進行匹配


        Arguments:
            img1 --你要在那張圖片上找
            imgF -- 查找用圖片

        Keyword Arguments:
            ORB -- 圖像算法器 (default: {cv2.SIFT.create(1000)})
            matcher -- 匹配器 (default: {cv2.BFMatcher()})
            confi -- 差距值 (default:0.7)

        Return: List
            [0] List 存儲找到的點

            [1] -> [0]KP1 [1] KP2 (包含kp&des)

        """
        
        #查找用
        KP1=cv2Tool.GetKP(imgF,SIFT=ORB)
        #截圖
        KP2=cv2Tool.GetKP(img1,SIFT=ORB)

        if KP1[1] is None or KP2[1] is None:
            print("沒有找到特徵")
            return None
        
        matcher_bf=matcher.knnMatch(KP1[1],KP2[1],k=2)
        
        good=[]
        for m,n in matcher_bf:
            if m.distance < confi*n.distance:
                good.append([m])
        

        Result=[
            good,
            [KP1,KP2],

        ]
        if len(good)>=1:
            FindP=KP2[0][good[0][0].trainIdx].pt
            print(f'找到的點:{FindP}')


        print(f'找到的數量:{len(good)}')
        
        return Result
        

    def GetKP(img,Mask=None,SIFT=cv2.SIFT_create()):
        """GetKP 取得關鍵點與特徵

        Arguments:
            img -- 圖片數據Image

            Mask -- 指定檢測的關鍵點

        Keyword Arguments:
            SIFT -- 創建器 (default: {cv2.SIFT_create()})

        Returns: List
            [0] Keypoints 關鍵點

            [1] Descriptors 特徵
        """
        kp,des=SIFT.detectAndCompute(img,Mask)

        return [kp,des]


class GetItem: 
    """主要進行統計加減值"""

    def __init__(self):
        """初始化"""
        self.Hour=0
        self.Play=0
        self.xp={   
                    'Count':0,
                    '5KCount':0,
                    '1WCount':0,
                    '3WCount':0,
                    '5WCount':0,
                    'Value':0
                }
        self.feed={'Count':0,'Value':0}
        self.CC=0
        self.Rest=False
        

    def __str__(self) -> str:
        return f'已探險{self.Play}次 共{self.Hour}小時 '
    


    def AddXP(self,value,Type_D='Count'):
        """
        value -- 增加xp值
        type -- xp字典分類(default:Count) 
            Dict:(5W/3W/1W/5K)Count/Count
            Ex:5WCount/3WCount..

        增加xp次數&給定xp
        """  
        self.xp['Value']+=value
        self.xp[Type_D]+=1


    def AddFeed(self,value):
        """增加罐頭次數&給定罐頭"""
        self.feed['Value']+=value
        self.feed['Count']+=1


    def Range(self):
        """獲得統計概率 回傳為字典"""
        All=self.xp['Count']+self.feed['Count']
        if All==0:return None
        XPRange=round((self.xp['Count']/All)*100)
        FeedRange=round((self.feed['Count']/All)*100)

        return {'XP':XPRange,'Feed':FeedRange,'Count':All}


    def Result(self):
        """獲得統計數量"""
        return f"""
        已探險{self.Play}次
        獲得 xp:{self.xp['Count']}次 +{self.xp['Value']} 貓罐頭:{self.feed['Count']}次 +{self.feed['Value']}
        共{self.Hour}小時 元寶 得到:{self.CC}個
        """
    

    def ResultH(self):
        """獲得統計數量(只取xp&貓罐頭) 和次數"""
        return f"獲得 xp:{self.xp['Count']}次 +{self.xp['Value']} 貓罐頭:{self.feed['Count']}次 +{self.feed['Value']} 已探險{self.Play}次 共{self.Hour}小時"


# Item=GetItem()
# Item.AddXP(300)
# Item.AddXP(900)
# print(Item.Result())
