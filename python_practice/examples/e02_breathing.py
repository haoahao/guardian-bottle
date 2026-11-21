# E02【單一模組｜LED】手機呼吸通知燈
# 生活情境：手機有未讀訊息時，燈會慢慢變亮、再慢慢變暗，像在呼吸。
# 學到：PWM（用很快的開關控制亮度）、range 的第三個數字（間隔）
# 接線：GP15 → 220Ω → LED 長腳，短腳 → GND

from machine import Pin, PWM
import time

led = PWM(Pin(15))
led.freq(1000)                   # 每秒開關 1000 次，眼睛看不出閃

for breath in range(3):          # 呼吸 3 次
    for d in range(0, 65536, 2048):        # 漸亮：0 → 65535
        led.duty_u16(d)
        time.sleep_ms(30)
    for d in range(65535, -1, -2048):      # 漸暗
        led.duty_u16(d)
        time.sleep_ms(30)
led.duty_u16(0)
