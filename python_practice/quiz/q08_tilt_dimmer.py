# Q08【雙模組｜MPU6050＋LED】傾斜感應夜燈
# 生活情境：把夜燈越往下歪，燈就越亮（0° 全暗、90° 最亮）。
# 要求：
#   1. 先校準記住平放方向
#   2. 傾斜角換成亮度：duty = 傾斜角 / 90 × 65535
#   3. 超過 90° 就當 90°，每 0.1 秒更新一次
# 提示：min(t, 90) 可以把數字上限卡在 90；duty 要轉成 int。
# 接線：GP15 → 220Ω → LED 長腳，短腳 → GND
# 接線：MPU6050 VCC→3V3  GND→GND  SDA→GP4  SCL→GP5（Pico W 裡要有 mpu6050.py、guardian.py）

from machine import Pin, I2C
import time
from mpu6050 import MPU6050
from guardian import magnitude, tilt_deg, calibrate

i2c = I2C(0, sda=Pin(4), scl=Pin(5), freq=400000)
mpu = MPU6050(i2c, g_range=8)
from machine import PWM
led = PWM(Pin(15))
led.freq(1000)

REF = calibrate(mpu)
while True:
    t = tilt_deg(mpu.accel(), REF)
    # TODO：把 t 換成 duty 設定亮度
    time.sleep(0.1)
