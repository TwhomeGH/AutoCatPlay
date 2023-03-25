# AutoCatPlay 自動化貓戰

## 本項目主要分為以下

* 自動化加碼多多的
* 戰鬥AI(目前這個運行方式並非AI)


# 按鍵指南

連續點擊ESC 5次以上可以退出進程  
按G鍵 可以開關 戰鬥AI  
(如果你正在遊戲中 他能識別一些貓 並自動點擊他)  
該功能不完整 只有img/Play裡的貓能識別(待完善)  


# 檔案說明

Auto.py 主要程式
CatFeed.py 統計數據的類配置
Capture.py 用來截取多張圖片(用於多張查找用)
imageT.py 這是我當時測試easyocr取得文字用的

# 資料夾說明

* Get 用於在得到物品 存下圖片
這是我打算自動蒐集得到物品樣本用的

* Shot 這是使用Capture截取下來的圖片存儲位置
* img 主要查找用圖片存放



# 依賴庫Requirements:


## 可以使用此文件->requirements.txt
- PyAutoGUI==0.9.53
- pillow==9.4.0 (PyAutoGUI需要)
- opencv==4.7.0.42 (PyAutoGUI需要(使用到相似度的部分))
- PyDirectInput==1.0.4
- pynput==1.7.6
- win32gui==221.6

## 其他可以使用此->Other.txt
* easyocr==1.6.2(可略過 只有imageT會用到)



# 運行注意事項

* 以下這段代碼 可以去掉
`with open('C:/Users/u01/Desktop/NuclearWeb/Status.txt', 'w') as f:
                    DictR=ItemGet.Range()
                    Range='探險數據不夠統計..'
                    if DictR:
                        Range=f"得到XP:{DictR.get('XP')}% 得到罐頭:{DictR.get('Feed')}%"

                    f.write(f"""
                    E1{ItemGet.ResultH()}E2
                    E3{Range}E4
                    """
                    )`s

這只是我用來寫入到網站根目錄下的一個檔案
用來給Siri捷徑 訪問網站下的指定檔案 獲取文字內容
來方便從iPad上查看統計數據

