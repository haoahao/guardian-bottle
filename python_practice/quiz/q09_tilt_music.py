# Q09【雙模組｜MPU6050＋蜂鳴器】體感電子樂器
# 生活情境：像玩體感遊戲：把麵包板歪越多，音越高。
# 要求：
#   1. 先校準
#   2. 傾斜 0°～90° 對應 262～1047 Hz
#   3. 傾斜小於 5° 時靜音，每 0.05 秒更新
# 提示：freq = 262 + 傾斜角 / 90 × (1047 − 262)。
# 接線：蜂鳴器模組 S → GP14、VCC → 3V3、GND → GND
# 接線：MPU6050 VCC→3V3  GND→GND  SDA→GP4  SCL→GP5（Pico W 裡要有 mpu6050.py、guardian.py）

from machine import Pin, I2C
import time
from mpu6050 import MPU6050
from guardian import magnitude, tilt_deg, calibrate

i2c = I2C(0, sda=Pin(4), scl=Pin(5), freq=400000)
mpu = MPU6050(i2c, g_range=8)
from machine import PWM
buzzer = PWM(Pin(14))

REF = calibrate(mpu)
while True:
    t = min(tilt_deg(mpu.accel(), REF), 90)
    # TODO：t < 5 靜音；否則換算頻率並發聲
    time.sleep(0.05)
