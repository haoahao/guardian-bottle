# Q10【雙模組｜MPU6050＋LED】計步器
# 生活情境：手環計步：每走一步會有一次加速度高峰。
# 要求：
#   1. 總加速度大於 1.3 g 算一步，LED 閃 0.1 秒並印出步數
#   2. 要等總加速度回到 1.1 g 以下，才能算下一步（避免一步算兩次）
#   3. 拿著麵包板上下晃 10 次，看步數準不準
# 提示：用一個變數 ready = True/False 記住「可不可以算下一步」。
# 接線：GP15 → 220Ω → LED 長腳，短腳 → GND
# 接線：MPU6050 VCC→3V3  GND→GND  SDA→GP4  SCL→GP5（Pico W 裡要有 mpu6050.py、guardian.py）

from machine import Pin, I2C
import time
from mpu6050 import MPU6050
from guardian import magnitude, tilt_deg, calibrate

i2c = I2C(0, sda=Pin(4), scl=Pin(5), freq=400000)
mpu = MPU6050(i2c, g_range=8)
led = Pin(15, Pin.OUT)

steps = 0
ready = True
while True:
    m = magnitude(mpu.accel())
    # TODO：ready 且 m > 1.3 → 算一步；m < 1.1 → ready 變回 True
    time.sleep_ms(20)
