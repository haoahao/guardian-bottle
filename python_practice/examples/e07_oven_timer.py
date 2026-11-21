# E07【雙模組｜LED＋蜂鳴器】烤箱倒數計時器
# 生活情境：烤箱倒數時每秒閃一下、嗶一聲；時間到長響一聲。
# 學到：倒數的 range(5, 0, -1)、兩個模組同時動作、函式
# 接線：LED 接 GP15（經 220Ω），蜂鳴器 S 接 GP14

from machine import Pin, PWM
import time

led = Pin(15, Pin.OUT)
buzzer = PWM(Pin(14))
buzzer.freq(1500)

def tick(sec):
    led.on()
    buzzer.duty_u16(20000)
    time.sleep(sec)
    led.off()
    buzzer.duty_u16(0)

for n in range(5, 0, -1):        # 5、4、3、2、1
    print("剩", n, "秒")
    tick(0.1)
    time.sleep(0.9)
print("時間到！")
tick(1.5)                        # 長響
