# D10【函式 def、return】寫出跌倒判斷函式
# 題目：把守護瓶的規則包成函式，之後 main.py 就能直接呼叫。
# 要求：
#   1. magnitude(ax, ay, az) 回傳總加速度
#   2. is_fall(peak, tilt) 在 peak > 2.5 且 tilt > 60 時回傳 True，否則 False
#   3. 用下面三組測資測試
# 執行後 Shell 應該看到（多一個、少一個空格沒關係）：
#   總加速度 1.0
#   True
#   False
#   False
# 不用接任何零件，Thonny 右下角選 Local Python 3 就能跑。
# 做完存檔。做完 D05、D10 各上傳一次到 groups/你們組/（見 drills/README.md）。

def magnitude(ax, ay, az):
    # TODO：回傳 (ax² + ay² + az²) 開根號
    pass

def is_fall(peak, tilt):
    # TODO：兩個條件都成立才回傳 True（用 and）
    pass

print("總加速度", round(magnitude(0.6, 0, 0.8), 2))
print(is_fall(3.2, 85))   # 撞擊大、躺平
print(is_fall(3.2, 10))   # 撞擊大、但還站著（例如被敲一下）
print(is_fall(1.1, 85))   # 慢慢放倒，沒有撞擊
