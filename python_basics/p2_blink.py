# p2_blink.py — import、for 迴圈、time.sleep：讓 LED 閃爍
# 接線：GP15 → 220Ω → LED 長腳，短腳 → GND

from machine import Pin    # import：借用別人寫好的工具
import time

led = Pin(15, Pin.OUT)     # 第 15 支腳設成「輸出」

for i in range(3):         # 重複 3 次：i 依序是 0、1、2
    print("第", i + 1, "次")
    led.on()               # 亮
    time.sleep(0.5)        # 等 0.5 秒
    led.off()              # 暗
    time.sleep(0.5)

print("閃完了")

# 小挑戰 1：讓 LED 閃 5 次。
# 小挑戰 2：閃快一倍（等待時間要改成多少？）。
