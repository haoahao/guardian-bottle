# guardian.py — 守護瓶共用工具：總加速度、傾斜角、站立校準
# main.py 和 collect.py 都用這裡的函式，確保規則版和 AI 資料用同一套算法。

import math, time

SAMPLE_HZ = 50                 # 全課程統一 50 Hz
PERIOD_MS = 1000 // SAMPLE_HZ


def magnitude(a):
    """總加速度：不管怎麼擺，靜止時都約等於 1 g（就是重力）。"""
    return math.sqrt(a[0] * a[0] + a[1] * a[1] + a[2] * a[2])


def tilt_deg(a, ref):
    """現在的重力方向和站立時差幾度：0° 站著，90° 躺平。和麵包板怎麼綁無關。"""
    m1, m2 = magnitude(a), magnitude(ref)
    if m1 < 0.2 or m2 < 0.2:
        return 0.0              # 讀值太小（例如正在掉落），先不判斷
    c = (a[0] * ref[0] + a[1] * ref[1] + a[2] * ref[2]) / (m1 * m2)
    c = max(-1.0, min(1.0, c))
    return math.acos(c) * 180 / math.pi


def calibrate(mpu, oled=None):
    """站立校準：瓶子要站好不動 2 秒。沒站穩就重來，直到成功。"""
    while True:
        if oled:
            oled.fill(0)
            oled.text("Calibrating...", 0, 16)
            oled.text("stand it upright", 0, 32)
            oled.text("don't touch", 0, 44)
            oled.show()
        xs = []
        n = SAMPLE_HZ * 2
        for _ in range(n):
            xs.append(mpu.accel())
            time.sleep_ms(PERIOD_MS)
        ref = tuple(sum(v[k] for v in xs) / n for k in range(3))
        ms = [magnitude(v) for v in xs]
        mean = sum(ms) / n
        sd = math.sqrt(sum((m - mean) ** 2 for m in ms) / n)
        if sd < 0.05 and 0.85 < mean < 1.15:
            print("站立校準完成，重力方向：(%.2f, %.2f, %.2f)" % ref)
            return ref
        print("校準失敗（晃動 %.3f g、平均 %.2f g），請把瓶子立好不要碰，重新校準" % (sd, mean))
        if oled:
            oled.fill(0)
            oled.text("Not steady!", 0, 20)
            oled.text("retry in 2 s", 0, 36)
            oled.show()
        time.sleep_ms(2000)
