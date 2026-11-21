# Q01【單一模組｜LED】求救燈 SOS
# 生活情境：登山迷路時，用手電筒打摩斯密碼 SOS：短短短、長長長、短短短。
# 要求：
#   1. 短閃亮 0.2 秒、長閃亮 0.6 秒，每次閃完暗 0.2 秒
#   2. 三個字母之間多停 0.6 秒
#   3. 整組 SOS 重複 2 次
# 提示：寫一個 flash(sec) 函式，再用串列 [0.2,0.2,0.2,0.6,0.6,0.6,0.2,0.2,0.2] 走一遍。
# 接線：GP15 → 220Ω → LED 長腳，短腳 → GND

from machine import Pin
import time

led = Pin(15, Pin.OUT)

# TODO 1：寫 flash(sec)：亮 sec 秒、暗 0.2 秒

# TODO 2：用串列和 for 迴圈打出 SOS，重複 2 次
