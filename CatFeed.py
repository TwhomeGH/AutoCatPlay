"""
用於統計得到物品用
"""

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
