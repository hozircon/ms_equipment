import pyautogui
import pydirectinput
import time
import threading
import msvcrt
import sys
import os
from PIL import Image

# 全域旗標
running = True
pydirectinput.PAUSE = 0

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

# 支援的屬性圖片
attribute_imgs = {
    "STR": {"3": "str3.png", "6": "str6.png"},
    "DEX": {"3": "dex3.png", "6": "dex6.png"},
    "INT": {"3": "int3.png", "6": "int6.png"},
    "LUK": {"3": "luk3.png", "6": "luk6.png"},
    "ALL": {"3": "all3.png"}  # all3% 特殊屬性
}



def detect_attribute():
    """
    每輪先截圖，再對所有模板比對
    """
    result = {attr:0 for attr in attribute_imgs}
    screenshot = pyautogui.screenshot(region=region)  # 截圖一次

    for attr, files in attribute_imgs.items():
        for val, filename in files.items():
            filepath = os.path.join(ATTRIBUTE_PATH, filename)
            try:
                template = Image.open(filepath)
                if pyautogui.locate(template, screenshot, confidence=0.95):
                    result[attr] += int(val)
                    print(f"檢測屬性 {attr} : {val}%")
            except:
                pass

    return result

def should_stop(mode, detected, target_attr=None):
    """
    根據模式判斷是否達成停止條件
    """
    if mode == 2:  # 任意屬性 >= 9%
        return any(val >= 9 for val in detected.values())
    elif mode == 3 and target_attr:  # 指定屬性 >= 9%
        return detected.get(target_attr.upper(), 0) >= 9
    return False

def find_and_press(mode, target_attr=None):
    global running
    while running:
        time.sleep(0.1)

        # mode 1：原始 normal.png 機制
        if mode == 1:
            try:
                # 偵測 normal.png
                normal_found = pyautogui.locateCenterOnScreen(normal, region=region, confidence=0.8)
                if normal_found:  # 找到 normal
                    try:
                        x1, y1 = pyautogui.locateCenterOnScreen(agin_new, region=region, confidence=0.7)
                        if x1 and y1:
                            pydirectinput.click(x1, y1- 80)
                            time.sleep(0.01)
                            pydirectinput.press("space")
                            time.sleep(0.05)
                            pydirectinput.press("space")
                            time.sleep(0.5) # 等待畫面更新，再少會偵測到更新前畫面
                    except pyautogui.ImageNotFoundException:
                        print(f"未能找到圖像：{agin_new}")
            except pyautogui.ImageNotFoundException:
                print("normal.png 圖片不存在或讀取失敗")
            except Exception as e:
                print(f"其他錯誤: {str(e)}")
            continue

        # mode 2 / mode 3：進階屬性篩選

        try:
            # 偵測 normal.png
            special_found = pyautogui.locateCenterOnScreen(special, region=region, confidence=0.8)
            if special_found:  # 找到 special
                detected = detect_attribute()
                print("屬性偵測結果:", detected)

                if should_stop(mode, detected, target_attr):
                    print("達成停止條件，結束程式")
                    running = False
                    break
                else:
                    try:
                        x1, y1 = pyautogui.locateCenterOnScreen(agin_new, region=region, confidence=0.7)
                        if x1 and y1:
                            pydirectinput.click(x1, y1- 80)
                            time.sleep(0.01)
                            pydirectinput.press("space")
                            time.sleep(0.05)
                            pydirectinput.press("space")
                            time.sleep(0.5) # 等待畫面更新，再少會偵測到更新前畫面
                    except pyautogui.ImageNotFoundException:
                        print(f"未能找到圖像：{agin_new}")
        except pyautogui.ImageNotFoundException:
            print("special.png 圖片不存在或讀取失敗")
        except Exception as e:
            print(f"其他錯誤: {str(e)}")
        continue


def listen_for_exit():
    global running
    while running:
        if msvcrt.kbhit():
            key = msvcrt.getch()
            if key == b'\x1b':  # ESC
                print("偵測到 ESC → 結束程式")
                running = False
                break


def main(mode, target_attr=None):
    match mode:
        case 1:
            print("mode = ",mode," 跳稀有")
        case 2:
            print("mode = ",mode," 稀有洗隨機9%以上屬性")
        case 3:
            print("mode = ",mode," 稀有洗{target_attr}9%以上屬性")

    global running
    listener = threading.Thread(target=listen_for_exit, daemon=True)
    listener.start()

    try:
        # find_and_click(mode=mode, target_attr=target_attr)
        find_and_press(mode=mode, target_attr=target_attr)
    except KeyboardInterrupt:
        print("偵測到 Ctrl+C → 結束程式")
        running = False
    finally:
        print("程序已停止")
        sys.exit(0)


if __name__ == '__main__':
    # 預設參數
    mode = 1
    target_attr = None

    # 命令列參數解析
    args = sys.argv[1:]
    if len(args) >= 1:
        try:
            mode = int(args[0])
        except ValueError:
            print("模式必須是數字 (1, 2, 3)")
            sys.exit(1)

    if len(args) == 2:
        target_attr = args[1].upper()  # 轉大寫，避免大小寫問題

    print(f"啟動模式: {mode}, 屬性: {target_attr if target_attr else '無'}")
    main(mode=mode, target_attr=target_attr)
