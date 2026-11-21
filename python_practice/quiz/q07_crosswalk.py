# Q07【雙模組｜LED＋蜂鳴器】行人號誌倒數
# 生活情境：過馬路時，綠燈最後幾秒小綠人跑得越來越快，還會嗶嗶提醒。
# 要求：
#   1. 倒數 10 秒：前 5 秒 LED 恆亮
#   2. 最後 5 秒 LED 每秒閃 2 下並嗶 2 聲
#   3. 印出剩下秒數，時間到 LED 熄滅
# 提示：for n in range(10, 0, -1)，用 if n > 5 分成兩種動作，每圈總共要剛好 1 秒。
# 接線：GP15 → 220Ω → LED 長腳，短腳 → GND
# 接線：蜂鳴器模組 S → GP14、VCC → 3V3、GND → GND

from machine import Pin, PWM
import time

led = Pin(15, Pin.OUT)
buzzer = PWM(Pin(14))
buzzer.freq(2000)

for n in range(10, 0, -1):
    print('剩', n, '秒')
    # TODO：n > 5 恆亮 1 秒；否則閃 2 下、嗶 2 聲（合計 1 秒）

led.off()
