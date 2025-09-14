# 洗陶德裝備魔法

## 功能說明
- **Mode 1**：基礎模式：把裝備從特殊洗到稀有即停止  
- **Mode 2**：進階屬性篩選：將稀有裝備洗到「隨機」屬性9%或以上時停止  
- **Mode 3**：指定屬性篩選：將稀有裝備洗到「指定」屬性9%或以上時停止

## 安裝方式
1. 安裝 Python 3.8+  
2. 下載專案後，安裝需求套件：
   ```bash
   pip install -r requirements.txt
    ```
## 啟動方式：
0. 需要視窗化遊戲，視窗盡量擺在左上角，要停止時滑鼠點擊cmd視窗連續點ESC 或者使用Ctrl + C來強制結束
1. 調整系統調整區以符合執行環境，主要調整腳本圖片路徑即可  
必要時重新截圖覆蓋原圖檔或調整腳本內的confidence相似度
    ```python
    ## ============ 系統調整區 ============
    # 監控範圍
    region = (0, 0, 2330, 1540)

    # 強化介面UI圖片路徑
    normal = r"E:\ms_equipment\sys\normal.png"
    special = r"E:\ms_equipment\sys\special.png"
    agin_new = r"E:\ms_equipment\sys\agin_new.png"
    # 屬性圖片路徑
    ATTRIBUTE_PATH = r"E:\ms_equipment\attribute"

    ## ====================================
    ```

2. 使用管理者權限開啟cmd介面

### Mode 1：基礎模式
```
python main.py 1
```

### Mode 2：進階屬性篩選
```
python main.py 2
```
### Mode 3：指定屬性篩選 (STR / DEX / INT ...)
```
python main.py 3 STR
python main.py 3 DEX
python main.py 3 LUK
python main.py 3 INT
```

