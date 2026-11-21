# p3_buzzer.py — 串列（list）、用 for 走過串列：讓蜂鳴器唱歌
# 接線（Keyes 蜂鳴器模組 3 支腳）：S → GP14、VCC → 3V3、GND → GND

from machine import Pin, PWM
import time

buzzer = PWM(Pin(14))

notes = [262, 294, 330, 349, 392]   # Do Re Mi Fa Sol 的頻率（Hz）

for f in notes:            # f 依序拿到串列裡的每一個數字
    print("頻率", f, "Hz")
    buzzer.freq(f)         # 設定音高
    buzzer.duty_u16(20000) # 出聲（音量）
    time.sleep(0.3)
    buzzer.duty_u16(0)     # 靜音
    time.sleep(0.05)

# 小挑戰：設計你們組的「跌倒警報聲」。
# 提示：高音、低音交替，例如 [2000, 1000, 2000, 1000]，會比較像警報嗎？
