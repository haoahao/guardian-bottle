# Q04【單一模組｜蜂鳴器】倒車雷達
# 生活情境：倒車越靠近牆，嗶嗶聲越急，最後變成長音。
# 要求：
#   1. 間隔依序 0.8、0.5、0.3、0.15 秒，每種間隔嗶 4 聲
#   2. 每聲嗶 0.08 秒
#   3. 最後長響 1 秒
# 提示：外層 for 走間隔串列，內層 for 嗶 4 聲。
# 接線：蜂鳴器模組 S → GP14、VCC → 3V3、GND → GND

from machine import Pin, PWM
import time

buzzer = PWM(Pin(14))
buzzer.freq(1800)
gaps = [0.8, 0.5, 0.3, 0.15]

# TODO：兩層 for 迴圈做出越來越急的嗶聲，最後長響
