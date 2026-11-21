# D08【for＋if、計數】撞擊幾次？在哪裡？
# 題目：找出超過門檻的讀數有幾筆，並記下它們是第幾筆。
# 要求：
#   1. count 記次數
#   2. 用 enumerate 同時拿到「第幾筆」和數值
#   3. 印出每一次撞擊的位置
# 執行後 Shell 應該看到（多一個、少一個空格沒關係）：
#   第 6 筆：3.8 g
#   第 7 筆：2.1 g
#   撞擊共 2 次
# 不用接任何零件，Thonny 右下角選 Local Python 3 就能跑。
# 做完存檔。做完 D05、D10 各上傳一次到 groups/你們組/（見 drills/README.md）。

readings = [1.0, 1.0, 0.9, 0.4, 0.3, 3.8, 2.1, 1.1, 1.0]
TH = 2.0
count = 0
for i, m in enumerate(readings, 1):
    # TODO：超過 TH 就 count 加 1 並印出位置
    pass
# TODO：印出總次數
