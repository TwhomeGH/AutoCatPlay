# AutoCatPlay 自動化貓戰

## 本項目主要分為以下

* 自動化加碼多多的
* 戰鬥AI(目前這個運行方式並非AI)


# 可能存在問題
當視窗大小分辨率不同時 可能檢測不到

# 新增特性

添加動態窗口百分比放大或縮小的功能  
此功能可以改善分辨率不同時檢測不到的問題

# 動態調整縮放圖片百分比

此方法只有使用get_xy/MoreSearch  
指定Mode=1/Mode_=1時會使用  

此功能會由`cv2Scale`方法進行  
需要指定窗口`SearchWin`的窗口標題

`cv2Scale`方法 如果可以找到已經調整過的樣本  
則會直接計算差異 確認是否需要再重新調整  
否則直接返回已存在檔案位置


# 按鍵指南

* Auto.py  
<kbd>ESC</kbd> 重複點擊5次此按鍵 可以退出進程   
<kbd>C</kbd> 可以開關 戰鬥AI  
<kbd>H</kbd> 可以取得鼠標位置(用來確認Region範圍用的)  
<kbd>V</kbd> 重複點擊5次此按鍵 測試Resize圖片  
    <kbd>-</kbd> <kbd>+</kbd>  快捷降低/增加延遲間隔
    <kbd>Num3</kbd> 快捷降低接替間隔  
    <kbd>M</kbd> 用來取得指定窗口區域
    <kbd>L</kbd> 測試探險策略
    <kbd>P</kbd> 測試滑鼠click Mode1

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
間隔最高到 60秒(目前)

# 檔案說明

* Auto.py 主要程式
* CatFeed.py 統計數據的類配置
* Capture.py 用來截取多張圖片(用於多張查找用)
* Thread.py 之前用來測試多線程的
* imageT.py 這是我當時測試easyocr取得文字用的

# 資料夾說明

* Resize 動態更新圖片專用的存儲資料夾
> 重新調整過大小圖片 會順著原圖片檔案上層目錄
> 檢查此資料夾是否存在 並存放調整後圖片在此資料夾內


* Get 用於在得到物品 存下圖片
> Screen.txt 是關於截圖時 窗口區域信息
> 這是我打算自動蒐集得到物品樣本用的

* Shot 這是使用Capture截取下來的圖片存儲位置
* img 主要查找用圖片存放



# 依賴庫Requirements:


## 可以使用此文件->requirements.txt
- PyAutoGUI==0.9.53
- pillow==9.4.0 
> PyAutoGUI需要
- opencv_python==4.7.0.42
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
WebFile="C:/Users/u01/Desktop/NuclearWeb/Status.json"
```

| WebFile 值 | 說明 |
| --- | --- |
| None | 略過寫入指定檔案 |
| String | 要寫入的檔案路徑(格式:json檔案) |

用來給Siri捷徑 訪問網站下的指定檔案 獲取文字內容   
來方便從iPad上查看統計數據

>> 現在結果以JSON字典保存


## 關於KeySet - Auto.py
```
KeySet={
    'Exit':keyboard.Key.esc,
    'Auto':keyboard.KeyCode.from_char('g'),
    'Point':keyboard.KeyCode.from_char('h')
    ...
}
```

| KeySet 字典值 | 快捷鍵說明 |
| --- | --- |
| Exit | 退出程序用的 |
| Auto | 戰鬥AI 開關 |
| Point | 獲取鼠標位置 |
| TestRisze | 測試重新縮放圖片 |
| -Delay | 減少運行間隔 |
| +Delay | 增加運行間隔 |
| AutoDelay | 降低接替間隔 |
| WinRect | 取得SearchWin的窗口區域 |
| HourList | 測試探險策略 |

現在你可以設定這個3個按鍵
你想要使用的按鍵了

## 關於一些變數 - Auto.py

```
SearchWin="雷電模擬器"
Debug=0
```


| SearchWin 值| 說明 | 用途 |
| --- | --- | --- |
| String | 窗口標題 | 以便於計算縮放百分比用 |


| Debug 值 | 說明 |
| --- | --- |
| 0 | 沒有调試輸出 |
| 1 | 簡易調適模式<br>這是調試期間 只打算進行鍵盤/滑鼠部分的調試用 |
| 2 | 測試戰鬥AI Region位置<br>以及click功能Debug |
| 3 | 不測試滑鼠(這可以讓你在進行斷點調適不造成卡頓) |


### click功能Debug
使用Mode=1時
會停用滑鼠與鍵盤的監聽

停用的監聽會在10秒後 啟用新線程