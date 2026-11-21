# E04【單一模組｜蜂鳴器】門鈴「叮～咚～」
# 生活情境：按門鈴，先高音再低音。
# 學到：串列（list）、zip 同時走兩個串列、自己寫函式 def
# 接線：蜂鳴器模組 S → GP14、VCC → 3V3、GND → GND

from machine import Pin, PWM
import time

buzzer = PWM(Pin(14))

def beep(freq, sec):
    """用 freq 赫茲響 sec 秒。"""
    buzzer.freq(freq)
    buzzer.duty_u16(20000)
    time.sleep(sec)
    buzzer.duty_u16(0)
    time.sleep(0.05)

notes = [659, 523]               # Mi（叮）、Do（咚）
times = [0.4, 0.8]
for f, t in zip(notes, times):
    beep(f, t)
