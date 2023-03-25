import threading as Th
import time


def T():
    time.sleep(5)
    print(f"5秒")



while True:
    a=Th.Thread(target=T)
    if a.is_alive()==False:
        a.start()
        print("線程不存在")
    else:
        print(a.is_alive)
    
    print(f"> {Th.active_count()}")
    time.sleep(2)