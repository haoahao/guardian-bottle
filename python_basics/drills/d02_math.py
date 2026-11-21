# D02【四則運算】感測器要存多少資料？
# 題目：守護瓶每秒讀 50 次，每次存 3 個數字（ax、ay、az）。
# 要求：
#   1. 算出 3 秒共讀幾次（samples）
#   2. 算出共存幾個數字（numbers）
#   3. 2.5 g 換成 m/s²（1 g = 9.8 m/s²）
# 執行後 Shell 應該看到（多一個、少一個空格沒關係）：
#   3 秒讀 150 次
#   共 450 個數字
#   2.5 g = 24.5 m/s²
# 不用接任何零件，Thonny 右下角選 Local Python 3 就能跑。
# 做完存檔。做完 D05、D10 各上傳一次到 groups/你們組/（見 drills/README.md）。

HZ = 50
seconds = 3
impact_g = 2.5
# TODO 1：samples = ?
# TODO 2：numbers = ?
# TODO 3：換算 m/s²，用 round(數字, 1) 取一位小數
