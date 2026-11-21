# E03【單一模組｜蜂鳴器】微波爐「叮！叮！叮！」
# 生活情境：微波爐加熱完成，響三聲提醒你。
# 學到：PWM 設定頻率（音高）、duty（有沒有聲音）
# 接線：蜂鳴器模組 S → GP14、VCC → 3V3、GND → GND

from machine import Pin, PWM
import time

buzzer = PWM(Pin(14))

for i in range(3):
    buzzer.freq(2000)            # 2000 Hz，高高的「叮」
    buzzer.duty_u16(20000)       # 出聲
    time.sleep(0.15)
    buzzer.duty_u16(0)           # 靜音
    time.sleep(0.35)
