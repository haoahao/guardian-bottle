# ============================================================
#  守護瓶任務｜樹莓派 AIoT 實作（Raspberry Pi Pico W + MPU6050）
#  臺北市立西松高中 115-1 週六微課程
# ============================================================
#  接線（與課程模板相同）
#    MPU6050 : VCC→3V3  GND→GND  SDA→GP4  SCL→GP5
#              （裝在瓶身的感測器艙裡，用 40 公分公母杜邦線接到桌上的麵包板）
#    OLED    : 2.42 吋，GND→GND  VDD→3V3  SCL→GP5  SDA→GP4（第一週可以先不接）
#    LED     : GP15 → 220Ω → LED 長腳，短腳→GND
#    蜂鳴器  : 模組 S→GP14、VCC→3V3、GND→GND
#
#  開機時請讓守護瓶「站好不動」2 秒：程式會記住「站立時重力的方向」。
#  所以感測器艙怎麼裝、MPU6050 朝哪個方向都可以，不必平放。
#  長線讀取不穩（偶爾 OSError）時，把下面 I2C 的 freq=400000 改成 100000。
#
#  把 STEP 改成 1、2、3：
#    STEP 1 感覺得到：看三軸加速度、總加速度、傾斜角度
#    STEP 2 規則判斷：撞擊＋倒下 → 跌倒警報
#    STEP 3 輸出設計：模擬 AI 的「標籤＋信心」，練習設計警報
# ============================================================

STEP = 1

from machine import Pin, I2C, PWM
import time, math
import ssd1306
from mpu6050 import MPU6050
from guardian import magnitude, tilt_deg, calibrate, SAMPLE_HZ, PERIOD_MS

i2c = I2C(0, sda=Pin(4), scl=Pin(5), freq=400000)
print("I2C 掃描到的裝置：", [hex(a) for a in i2c.scan()])  # 接了 OLED 會看到 0x3c 與 0x68；沒接只會看到 0x68
mpu = MPU6050(i2c, g_range=8)      # 跌倒撞擊常超過 4 g，所以用 ±8 g
class _NoOLED:                     # 沒接 OLED 時的替身：什麼都不做，程式照常跑
    def fill(self, *a): pass
    def text(self, *a): pass
    def show(self): pass

try:
    oled = ssd1306.SSD1306_I2C(128, 64, i2c)
except OSError:
    print("沒有接 OLED（或 OLED 沒回應），數字只顯示在 Shell")
    oled = _NoOLED()
led = Pin(15, Pin.OUT)
buzzer = PWM(Pin(14))
buzzer.duty_u16(0)


_buzz = [None]                      # 記住蜂鳴器目前的狀態


def beep(on, freq=2000):
    """只在狀態改變時才設定 PWM：每 20 ms 重設一次會讓聲音斷斷續續。"""
    want = freq if on else 0
    if want == _buzz[0]:
        return
    _buzz[0] = want
    if on:
        buzzer.freq(freq)
        buzzer.duty_u16(20000)
    else:
        buzzer.duty_u16(0)


REF = calibrate(mpu, oled)


# ------------------------------------------------------------
# STEP 1｜感覺得到
# 任務：搖一搖、放倒、用力放下，觀察 |a| 與 tilt 怎麼變。
# 想一想：守護瓶倒下的那一瞬間，|a| 會變大還是變小？
# ------------------------------------------------------------
def step1():
    print("ax ay az mag tilt")
    while True:
        a = mpu.accel()
        m = magnitude(a)
        t = tilt_deg(a, REF)
        oled.fill(0)
        oled.text("STEP1 sense", 0, 0)
        oled.text("X%+.2f Y%+.2f" % (a[0], a[1]), 0, 16)
        oled.text("Z%+.2f g" % a[2], 0, 28)
        oled.text("|a| %.2f g" % m, 0, 40)
        oled.text("tilt %3d deg" % t, 0, 52)
        oled.show()
        print("%.2f %.2f %.2f %.2f %.0f" % (a[0], a[1], a[2], m, t))
        time.sleep_ms(100)


# ------------------------------------------------------------
# STEP 2｜規則判斷（人寫規則的跌倒偵測）
# 規則：先有「撞擊」，撞擊後 1 秒還「倒著」→ 跌倒。
# 任務 1：調整三個門檻，讓推倒會叫、用力放下不會叫。
# 任務 2：把瓶子「慢慢放倒」，規則抓得到嗎？為什麼？
# 任務 3：記下規則會誤報、漏報的動作，下週和 AI 模型比較。
# ------------------------------------------------------------
TH_IMPACT = 2.5    # 撞擊門檻：總加速度超過幾 g 算撞擊
TH_TILT = 60       # 倒下門檻：和站立方向差幾度算倒下
TH_MOVE = 0.15     # 走動門檻：1 秒內總加速度的起伏（標準差）
POST_MS = 1000     # 撞擊後等多久再檢查姿勢


def step2():
    buf = []                 # 最近 1 秒的總加速度
    impact_at = None
    peak = 0.0               # 這次撞擊的最大值（給學生調門檻用）
    alarm = False
    upright_since = None
    last_state = None
    nxt = time.ticks_ms()
    print("state mag tilt   （只在狀態改變時印出）")
    while True:
        a = mpu.accel()
        m = magnitude(a)
        t = tilt_deg(a, REF)
        now = time.ticks_ms()
        buf.append(m)
        if len(buf) > SAMPLE_HZ:
            buf.pop(0)

        if m > TH_IMPACT:
            if impact_at is None:
                peak = 0.0
            impact_at = now
            peak = max(peak, m)
        if (not alarm and impact_at is not None
                and time.ticks_diff(now, impact_at) > POST_MS):
            print("撞擊 %.2f g，1 秒後傾斜 %d 度" % (peak, t))
            if t > TH_TILT:
                alarm = True          # 撞擊後仍倒著 → 跌倒
            impact_at = None

        if alarm:
            # 扶正並站穩 2 秒才解除警報
            if t < 30:
                upright_since = upright_since or now
                if time.ticks_diff(now, upright_since) > 2000:
                    alarm = False
                    upright_since = None
            else:
                upright_since = None

        if alarm:
            state = "FALL!"
        elif t > TH_TILT:
            state = "LYING"           # 倒著但沒有撞擊（慢慢放倒）
        else:
            mean = sum(buf) / len(buf)
            sd = math.sqrt(sum((x - mean) ** 2 for x in buf) / len(buf))
            state = "WALK" if sd > TH_MOVE else "STILL"

        blink = (now // 150) % 2 == 0
        led.value(1 if (alarm and blink) else 0)
        beep(alarm and blink, 2600)

        # OLED 更新一次約 25 ms，會拖慢取樣，所以只在狀態改變時更新
        if state != last_state:
            oled.fill(0)
            oled.text("STEP2 rules", 0, 0)
            oled.text(state, 0, 20)
            oled.text("peak %.2f g" % peak, 0, 40)
            oled.text("tilt %3d deg" % t, 0, 52)
            oled.show()
            print("%s %.2f %.0f" % (state, m, t))
            last_state = state

        nxt = time.ticks_add(nxt, PERIOD_MS)
        wait = time.ticks_diff(nxt, time.ticks_ms())
        if wait > 0:
            time.sleep_ms(wait)
        else:
            nxt = time.ticks_ms()


# ------------------------------------------------------------
# STEP 3｜輸出設計（第三堂預習）
# AI 模型會輸出「標籤＋信心分數」，例如 fall 0.92。
# 注意：這裡的「信心」是用規則算出來、我們自己編的數字，不是機率！
# 想一想：真正的模型說 fall 0.92，代表什麼？一定是跌倒嗎？
# 任務 1：信心低於 CONF_MIN 時顯示 "CHECK?"，請家人確認，而不是直接大叫。
# 任務 2：警報要響多久？什麼時候才可以停？（看 alarm 怎麼解除）
# ------------------------------------------------------------
CONF_MIN = 0.8


def fake_model(m_peak, t):
    """用規則假裝 AI：回傳 (標籤, 信心)。
    STEP 2 會警報的情況，信心至少 0.8；撞擊越大越接近 1。
    試試看把 CONF_MIN 調到 0.9：輕輕倒下的那幾次會變成 CHECK?"""
    if m_peak > TH_IMPACT and t > TH_TILT:
        conf = 0.8 + 0.2 * min(1.0, (m_peak - TH_IMPACT) / 2)
        return "fall", conf
    if t > TH_TILT:
        return "fall", 0.55             # 倒著但沒撞擊：不太確定
    return "still", 0.9


def step3():
    peak = 1.0
    peak_at = time.ticks_ms()
    alarm = False                       # 警報一旦響起就「閂住」，直到扶正
    upright_since = None
    last_text = None
    while True:
        a = mpu.accel()
        m = magnitude(a)
        t = tilt_deg(a, REF)
        now = time.ticks_ms()
        if m > peak or time.ticks_diff(now, peak_at) > 2000:
            peak, peak_at = m, now      # 記住最近 2 秒的最大撞擊
        label, conf = fake_model(peak, t)

        if label == "fall" and conf >= CONF_MIN:
            alarm = True
        if alarm:                       # 和 STEP 2 一樣：扶正站穩 2 秒才解除
            if t < 30:
                upright_since = upright_since or now
                if time.ticks_diff(now, upright_since) > 2000:
                    alarm = False
                    upright_since = None
            else:
                upright_since = None

        if alarm:
            text = "FALL! call help"
            led.value(1)
            beep(True, 2600)
        elif label == "fall":
            text = "CHECK? (unsure)"
            led.value((now // 500) % 2)
            beep(False)
        else:
            text = "OK"
            led.value(0)
            beep(False)
        if text != last_text:
            oled.fill(0)
            oled.text("STEP3 output", 0, 0)
            oled.text(text, 0, 24)
            oled.text("%s %.2f" % (label, conf), 0, 48)
            oled.show()
            print("%s  (%s %.2f)" % (text, label, conf))
            last_text = text
        time.sleep_ms(PERIOD_MS)


{1: step1, 2: step2, 3: step3}[STEP]()
