# E09【雙模組｜MPU6050＋蜂鳴器】機車防盜器
# 生活情境：停好的機車被人搖動，防盜器就叫。
# 學到：abs 絕對值、計數器變數、while True
# 接線：MPU6050（SDA→GP4、SCL→GP5），蜂鳴器 S 接 GP14

from machine import Pin, I2C, PWM
import time
from mpu6050 import MPU6050
from guardian import magnitude

i2c = I2C(0, sda=Pin(4), scl=Pin(5), freq=400000)
mpu = MPU6050(i2c, g_range=8)
buzzer = PWM(Pin(14))
buzzer.freq(2500)

TH = 0.3                         # 總加速度離 1 g 超過 0.3 就算被搖
alarms = 0
print("防盜啟動！輕輕搖麵包板試試")
while True:
    m = magnitude(mpu.accel())
    if abs(m - 1.0) > TH:
        alarms += 1
        print("被搖了！第", alarms, "次")
        for i in range(3):       # 嗶嗶嗶
            buzzer.duty_u16(25000)
            time.sleep(0.1)
            buzzer.duty_u16(0)
            time.sleep(0.1)
    time.sleep_ms(20)
