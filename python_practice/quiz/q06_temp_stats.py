# Q06【單一模組｜溫度感測器】氣象站每日統計
# 生活情境：氣象站會記錄一段時間的最高溫、最低溫和平均溫度。
# 要求：
#   1. 每 0.5 秒量一次，共量 10 次，存進串列
#   2. 印出最高、最低、平均（小數 1 位）
#   3. 量的時候可以用手指捏晶片，讓數字有變化
# 提示：串列可以用 append 加資料，max、min、sum、len 很好用。
# 接線：不用接線，溫度感測器在 Pico W 晶片裡

from machine import ADC
import time

sensor = ADC(4)

def read_temp():
    v = sensor.read_u16() * 3.3 / 65535
    return 27 - (v - 0.706) / 0.001721

data = []
# TODO 1：量 10 次存進 data

# TODO 2：印出最高、最低、平均
