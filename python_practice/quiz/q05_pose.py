# Q05【單一模組｜MPU6050】智慧手環判斷姿勢
# 生活情境：手環靠「重力在哪一軸」知道手是平放、立著還是翻過來。
# 要求：
#   1. 每 0.5 秒讀一次 ax、ay、az
#   2. az > 0.8 印「平放」；az < -0.8 印「翻面」；其他印「立著」
#   3. 同時印出三軸數值
# 提示：if / elif / else 三選一。先用 E05 看看平放時哪一軸接近 +1。
# 接線：MPU6050 VCC→3V3  GND→GND  SDA→GP4  SCL→GP5（Pico W 裡要有 mpu6050.py、guardian.py）

from machine import Pin, I2C
import time
from mpu6050 import MPU6050
from guardian import magnitude, tilt_deg, calibrate

i2c = I2C(0, sda=Pin(4), scl=Pin(5), freq=400000)
mpu = MPU6050(i2c, g_range=8)

while True:
    ax, ay, az = mpu.accel()
    # TODO：用 if / elif / else 判斷姿勢並印出
    time.sleep(0.5)
