# Q02【單一模組｜LED】檯燈五段調光
# 生活情境：觸控檯燈按一下亮一段，共 5 段：0%、25%、50%、75%、100%。
# 要求：
#   1. 用 PWM 控制亮度
#   2. 5 段亮度放在串列裡，每段停 1 秒
#   3. 每段印出「第 n 段：xx%」
# 提示：duty_u16 的最大值是 65535，50% 就是 65535 * 50 // 100。
# 接線：GP15 → 220Ω → LED 長腳，短腳 → GND

from machine import Pin, PWM
import time

led = PWM(Pin(15))
led.freq(1000)
levels = [0, 25, 50, 75, 100]

# TODO：走過 levels，算出 duty 並設定亮度、印出段數
