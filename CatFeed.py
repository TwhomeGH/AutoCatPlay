"""
用於統計得到物品用
"""

class GetItem: 
    """主要進行統計加減值"""

    def __init__(self):
        """初始化"""
        self.Play=0
        self.xp=0
        self.xpCount=0
        self.remReadxp=0
        self.feed=0
        self.feedCount=0
        self.CC=0
        self.Rest=False
        self.Hour=0


    def __str__(self) -> str:
        return self.xp


    def AddXP(self,value):
        """
        增加xp次數&給定xp
        """  
        self.xpCount+=value
        self.xp+=1


    def AddFeed(self,value):
        """增加罐頭次數&給定罐頭"""
        self.feedCount+=value
        self.feed+=1


    def Range(self):
        """獲得統計概率 回傳為字典"""
        All=self.xp+self.feed
        if All==0:return None
        XPRange=round((self.xp/All)*100)
        FeedRange=round((self.feed/All)*100)

        return {'XP':XPRange,'Feed':FeedRange,'Count':All}


    def Result(self):
        """獲得統計數量"""
        return f"""
        已探險{self.Play}
        獲得 xp:{self.xp}次 +{self.xpCount} 貓罐頭:{self.feed}次
        xpRemRead 得到:{self.remReadxp}
        元寶 得到:{self.CC}個
        共{self.Hour}小時
        """
    

    def ResultH(self):
        """獲得統計數量(只取xp&貓罐頭) 和次數"""
        return f"獲得 xp:{self.xp}次 +{self.xpCount} 貓罐頭:{self.feed}次 已探險{self.Play}次 共{self.Hour}小時"


# Item=GetItem()
# Item.AddXP(300)
# Item.AddXP(900)
# print(Item.Result())