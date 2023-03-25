# AutoCatPlay 自動化貓戰

## 本項目主要分為以下

* 自動化加碼多多的
* 戰鬥AI(目前這個運行方式並非AI)

# 存在問題
當你對視窗大小調整分辨率不同時  
可能檢測不到  
目前正在嘗試新增動態調整圖片識別的大小來識別  


# 按鍵指南

* Auto.py  
<kbd>ESC</kbd> 連續點擊5次以上可以退出進程   
<kbd>G</kbd> 可以開關 戰鬥AI  
<kbd>H</kbd> 可以取得鼠標位置(用來確認Region範圍用的)  

* Capture.py  
<kbd>G</kbd> 設置取樣點-1    
<kbd>H</kbd> 設置取樣點-2  

> (如果你正在遊戲中 他能識別一些貓 並自動點擊他)  
> 該功能不完整 只有img/Play裡的貓能識別(待完善)  

# 運行指南
* 裝好依賴庫後  
* 先看運行事項 修改Auto.py  
* 使用命令行運行以下命令運行主程式  

```
python Auto.py
```


# 運行特性

當你滑鼠或鍵盤持續點擊移動
會自動設為 非自動模式
> 命令行運行結果 狀態:0 非自動 1 自動

自動加碼多多只有在自動狀態下運行  

如果加碼多多正在探險 會增加運行間隔  
間隔最高到 120秒

# 檔案說明

* Auto.py 主要程式
* CatFeed.py 統計數據的類配置
* Capture.py 用來截取多張圖片(用於多張查找用)
* Thread.py 之前用來測試多線程的
* imageT.py 這是我當時測試easyocr取得文字用的

# 資料夾說明

* Get 用於在得到物品 存下圖片
> 這是我打算自動蒐集得到物品樣本用的

* Shot 這是使用Capture截取下來的圖片存儲位置
* img 主要查找用圖片存放



# 依賴庫Requirements:


## 可以使用此文件->requirements.txt
- PyAutoGUI==0.9.53
- pillow==9.4.0 
> PyAutoGUI需要
- opencv==4.7.0.42
> PyAutoGUI需要 使用到相似度的部分
- PyDirectInput==1.0.4
- pynput==1.7.6
- win32gui==221.6

## 其他可以使用此->Other.txt
* easyocr==1.6.2
> 可略過 只有imageT會用到



# 運行事項

## 運行分辨率信息
1920x1080 模擬器在視窗最大化下有效  
模擬器分辨率:1280x720


## 關於WebFile - Auto.py  
```
WebFile="C:/Users/u01/Desktop/NuclearWeb/Status.txt"
```
> 如果沒有打算在自架網站根目錄下寫入一個文字文件  
> 來方便你從Siri捷徑 來取得內容的話  
> 可以直接修改成  
```
WebFile=None
```
> 這會自動略過  
> 用來給Siri捷徑 訪問網站下的指定檔案 獲取文字內容   
> 來方便從iPad上查看統計數據

## 關於KeySet - Auto.py
```
KeySet={
    'Exit':keyboard.Key.esc,
    'Auto':keyboard.KeyCode.from_char('g'),
    'Point':keyboard.KeyCode.from_char('h')
}
```

> 現在你可以設定這個3個按鍵
> 你想要使用的按鍵了