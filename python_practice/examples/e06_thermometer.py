# E06【單一模組｜Pico 內建溫度感測器】教室溫度計
# 生活情境：電子溫度計每秒更新一次讀數。
# 學到：ADC（把電壓變數字）、算式換算、round
# 接線：不用接線！溫度感測器在 Pico W 晶片裡（ADC 第 4 通道）

from machine import ADC
import time

sensor = ADC(4)

def read_temp():
    v = sensor.read_u16() * 3.3 / 65535          # 0～65535 換成電壓
    return 27 - (v - 0.706) / 0.001721           # 官方換算公式

for i in range(10):
    print("第", i + 1, "次：", round(read_temp(), 1), "°C")
    time.sleep(1)
# 試試看：用手指捏住 Pico W 中間的黑色晶片，溫度會變嗎？
