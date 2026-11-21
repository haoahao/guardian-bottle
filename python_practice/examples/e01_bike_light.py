# E01【單一模組｜LED】腳踏車尾燈
# 生活情境：腳踏車尾燈「快閃兩下、停一下」，後面的車比較容易注意到。
# 學到：Pin 輸出、for 迴圈、time.sleep
# 接線：GP15 → 220Ω → LED 長腳，短腳 → GND

from machine import Pin
import time

led = Pin(15, Pin.OUT)

for round_ in range(5):          # 重複 5 輪
    for i in range(2):           # 每輪快閃 2 下
        led.on()
        time.sleep(0.1)
        led.off()
        time.sleep(0.1)
    time.sleep(0.6)              # 停一下
print("尾燈測試完成")
