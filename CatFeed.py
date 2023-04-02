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
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    def Thread(func,argsR=None):
        """Thread 運行新線程

        會運行func的內容

        Arguments:
            func -- 指定觸發函式
            argsR -- 傳遞給指定函式的參數
        """
        if argsR:
            T1=threading.Thread(target=func,args=argsR)
        else:T1 = threading.Thread(target=func)
        
        #print(T1.getName(),T1.is_alive())
        T1.start()

    def FindW(Class=None,Window=None):
        """
        用於指定窗口定位

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
                handle,
            ]
            return temp
    
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
    


class GetItem: 
    """主要進行統計加減值"""

    def __init__(self):
        """初始化"""
        self.Hour=0
        self.Play=0
        self.xp={'Count':0,'Value':0}
        self.feed={'Count':0,'Value':0}
        self.CC=0
        self.Rest=False
        

    def __str__(self) -> str:
        return f'已探險{self.Play}次 共{self.Hour}小時 '
    


    def AddXP(self,value):
        """
        增加xp次數&給定xp
        """  
        self.xp['Value']+=value
        self.xp['Count']+=1


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
        已探險{self.Play}
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
