# E10【雙模組｜溫度感測器＋LED】電暖器過熱警示
# 生活情境：電暖器太熱會亮警示燈，提醒你離遠一點。
# 學到：先量「基準」、和基準比較、模組之間用變數傳遞資料
# 接線：LED 接 GP15（經 220Ω）；溫度感測器在 Pico W 晶片裡

from machine import Pin, ADC
import time

sensor = ADC(4)
led = Pin(15, Pin.OUT)

def read_temp():
    v = sensor.read_u16() * 3.3 / 65535
    return 27 - (v - 0.706) / 0.001721

base = sum(read_temp() for i in range(20)) / 20      # 量 20 次取平均當基準
print("基準溫度 %.1f °C，用手指捏住晶片讓它變熱" % base)

while True:
    t = read_temp()
    if t > base + 2:             # 比基準高 2 °C 就警示
        led.on()
        print("過熱！ %.1f °C" % t)
    else:
        led.off()
    time.sleep(0.5)
