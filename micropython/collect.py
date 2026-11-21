# collect.py — 守護瓶資料蒐集（給 Edge Impulse 訓練用）
# 用法：
#   1. 修改下方 LABEL、GROUP，瓶子立在桌上，執行程式
#   2. 先站立校準 2 秒（不要碰瓶子）
#   3. 每一筆：嗶三聲倒數 → LED 亮起開始錄 3 秒 →「嗶！」高音時做動作
#      fall 請在高音響起時推倒（約第 1 秒），讓撞擊落在資料中間
#   4. 一次執行會連錄 REPEAT 筆；fall 每錄完一筆，把瓶子扶正就會自動接下一筆
#   5. 錄完後在 Thonny 左側「Raspberry Pi Pico」檔案區選取 .csv →
#      右鍵「下載到…」，再整批上傳 Edge Impulse
#
#   still ：瓶子站著不動、被輕碰、躺平不動
#   daily ：拿著走路、用力放到桌上、差點倒下又扶住（日常動作，不是跌倒）
#   fall  ：瓶子站在桌上，推倒到薄墊子上（全班用同一種墊子）
#   ※「慢慢放倒」不錄進全班共用的資料：各組自己決定它算哪一類，寫進成果
#
# 檔名如 fall.g1.03.csv，第一段（第一個「.」之前）就是標籤，Edge Impulse 會自動帶入。
# 每筆存 6 欄：timestamp、accX、accY、accZ（原始三軸），
#             mag（總加速度）、tilt（和站立方向的夾角）← 這兩欄和麵包板怎麼綁無關

from machine import Pin, I2C, PWM
import time, os
from mpu6050 import MPU6050
from guardian import magnitude, tilt_deg, calibrate, SAMPLE_HZ, PERIOD_MS

# ===== 每次錄製前改這裡 =====
LABEL = "fall"      # still / daily / fall
GROUP = "g1"        # 組別，寫進檔名避免各組檔案撞名
REPEAT = 5          # 這次連續錄幾筆
DURATION_MS = 3000  # 每筆 3 秒，Edge Impulse 用 2 秒視窗在裡面滑動
CUE_MS = 1000       # 第幾毫秒響「做動作」的高音
MIN_HZ = 47         # 實際取樣低於這個值就不存檔
# ============================

i2c = I2C(0, sda=Pin(4), scl=Pin(5), freq=400000)
mpu = MPU6050(i2c, g_range=8)     # 量程必須和第三堂推論程式相同
led = Pin(15, Pin.OUT)
bz = PWM(Pin(14))
bz.duty_u16(0)


def beep(ms=80, f=2000):
    bz.freq(f); bz.duty_u16(20000); time.sleep_ms(ms); bz.duty_u16(0)


def read():
    try:
        return mpu.accel()
    except OSError:               # 接線被撞鬆時 I2C 會偶爾失敗，重試一次
        time.sleep_ms(2)
        return mpu.accel()


def next_name():
    k = 1                          # 找第一個沒被用過的編號，不會覆蓋舊檔
    while True:
        name = "%s.%s.%02d.csv" % (LABEL, GROUP, k)
        try:
            os.stat(name)
            k += 1
        except OSError:
            return name


def wait_upright():
    """fall 錄完後，等瓶子被扶正並站穩 1 秒，才錄下一筆。"""
    print("請把瓶子扶正⋯")
    steady = 0
    while steady < SAMPLE_HZ:
        steady = steady + 1 if tilt_deg(read(), REF) < 20 else 0
        time.sleep_ms(PERIOD_MS)


def record_one():
    n = SAMPLE_HZ * DURATION_MS // 1000
    for _ in range(3):             # 倒數三聲
        beep()
        time.sleep_ms(600)
    rows = []
    cued = False
    led.value(1)
    t0 = time.ticks_ms()
    nxt = t0
    for _ in range(n):
        a = read()
        t = time.ticks_diff(time.ticks_ms(), t0)
        rows.append((t, a[0], a[1], a[2], magnitude(a), tilt_deg(a, REF)))
        if not cued and t >= CUE_MS:
            bz.freq(3200); bz.duty_u16(20000); cued = True   # 高音：做動作
        elif cued and t >= CUE_MS + 150:
            bz.duty_u16(0)
        nxt = time.ticks_add(nxt, PERIOD_MS)
        wait = time.ticks_diff(nxt, time.ticks_ms())
        if wait > 0:
            time.sleep_ms(wait)
    bz.duty_u16(0)
    led.value(0)
    return rows


REF = calibrate(mpu)
saved = 0
while saved < REPEAT:
    print("\n=== %s 第 %d/%d 筆 ===" % (LABEL, saved + 1, REPEAT))
    rows = record_one()
    real_hz = (len(rows) - 1) * 1000 / max(1, rows[-1][0])
    peak = max(r[4] for r in rows)
    end_tilt = rows[-1][5]
    print("實際 %.1f Hz　最大撞擊 %.2f g　結束時傾斜 %d 度" % (real_hz, peak, end_tilt))

    if real_hz < MIN_HZ:
        print("⚠ 取樣太慢，這筆不存，請重錄；一直發生請告訴老師")
        continue
    if LABEL == "fall" and end_tilt < 60:
        print("⚠ 瓶子好像沒有倒下，這筆不存，請重錄")
        wait_upright()
        continue

    name = next_name()
    with open(name, "w") as f:
        f.write("timestamp,accX,accY,accZ,mag,tilt\n")
        for i, r in enumerate(rows):
            # timestamp 用理想時間；實際頻率已在上面檢查過
            f.write("%d,%.4f,%.4f,%.4f,%.4f,%.1f\n" % (i * PERIOD_MS, r[1], r[2], r[3], r[4], r[5]))
    saved += 1
    print("已存成 %s" % name)
    if LABEL == "fall" and peak < 1.5:
        print("（撞擊很小：墊子太厚或推得太輕？記下來，可以和其他組比較）")
    if LABEL == "fall" and saved < REPEAT:
        wait_upright()
    else:
        time.sleep_ms(1500)

st = os.statvfs("/")
print("\n本次存了 %d 筆，板子剩餘空間約 %d KB" % (saved, st[0] * st[3] // 1024))
