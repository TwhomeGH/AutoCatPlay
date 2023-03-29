def log(*msg):
    """log 接收多個參數並打印
    
    使用方法:log(value1,value2,value..)
    value1,value2,value.. 可以是任何值可以一直往後增加
    """
    list(map(print,msg))
    
from CatFeed import *



log(WinTool.NowTime())

def Test():
    print("1")
    print("2")
    print("3")
    

WinTool.Thread(Test)


