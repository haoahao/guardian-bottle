# E08【雙模組｜MPU6050＋LED】水平儀
# 生活情境：掛畫、裝櫃子要用水平儀；歪了就亮燈提醒。
# 學到：校準（先記住「平的」方向）、tilt_deg 算傾斜角、if/else
# 接線：MPU6050（SDA→GP4、SCL→GP5），LED 接 GP15（經 220Ω）

from machine import Pin, I2C
import time
from mpu6050 import MPU6050
from guardian import tilt_deg, calibrate

i2c = I2C(0, sda=Pin(4), scl=Pin(5), freq=400000)
mpu = MPU6050(i2c, g_range=8)
led = Pin(15, Pin.OUT)

print("把麵包板平放在桌上不要動…")
REF = calibrate(mpu)             # 記住「平」的時候重力方向

TH = 10                          # 傾斜超過 10° 算「歪了」
while True:
    t = tilt_deg(mpu.accel(), REF)
    if t > TH:
        led.on()
        print("歪了 %d°" % int(t))
    else:
        led.off()
    time.sleep(0.1)
