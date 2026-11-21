# p5_sensor.py — while True、讀感測器、套用 if：撞一下就亮燈
# 先把 micropython/ 裡的 mpu6050.py 和 guardian.py 存進 Pico W，這支程式才找得到它們。
# 接線：MPU6050 VCC→3V3  GND→GND  SDA→GP4  SCL→GP5

from machine import Pin, I2C
import time
from mpu6050 import MPU6050
from guardian import magnitude

i2c = I2C(0, sda=Pin(4), scl=Pin(5), freq=400000)
mpu = MPU6050(i2c, g_range=8)
led = Pin(15, Pin.OUT)

TH = 1.5   # 門檻（g）：總加速度超過它就亮燈

while True:                  # 一直重複，直到按 Thonny 的「停止」
    a = mpu.accel()          # 讀三軸加速度 (ax, ay, az)
    m = magnitude(a)         # 算總加速度
    if m > TH:
        led.on()
        print("撞擊！ %.2f g" % m)
    else:
        led.off()
    time.sleep_ms(20)        # 每 20 毫秒讀一次，一秒 50 次

# 小挑戰 1：把 TH 改小，讓「輕拍桌子」也會亮燈。改成多少剛好？
# 小挑戰 2：改得太小會怎樣？這就是「誤報」。
