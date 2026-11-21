# E05【單一模組｜MPU6050】手機怎麼知道你轉了螢幕？
# 生活情境：手機裡也有加速度計，靠「重力在哪一軸」判斷你直拿或橫拿。
# 學到：import 自己的模組、讀感測器、%.2f 格式化
# 先把 micropython/ 的 mpu6050.py、guardian.py 存進 Pico W。
# 接線：MPU6050 VCC→3V3  GND→GND  SDA→GP4  SCL→GP5

from machine import Pin, I2C
import time
from mpu6050 import MPU6050
from guardian import magnitude

i2c = I2C(0, sda=Pin(4), scl=Pin(5), freq=400000)
mpu = MPU6050(i2c, g_range=8)

for i in range(50):              # 讀 50 次，約 5 秒
    ax, ay, az = mpu.accel()
    m = magnitude((ax, ay, az))
    print("X %+.2f  Y %+.2f  Z %+.2f  |a| %.2f g" % (ax, ay, az, m))
    time.sleep(0.1)
# 試試看：把麵包板立起來、側放，哪一軸會變成接近 1？
