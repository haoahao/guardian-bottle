# mpu6050.py — 精簡版 MPU6050 讀取模組（MicroPython）
# 只做這門課需要的事：喚醒、設定量程、讀三軸加速度（單位 g）。

ADDR = 0x68          # AD0 接地（預設）；AD0 接 3V3 時改成 0x69
PWR_MGMT_1 = 0x6B    # 電源管理：開機時是「睡眠」狀態，要寫 0 喚醒
ACCEL_CONFIG = 0x1C  # 加速度量程設定
ACCEL_XOUT_H = 0x3B  # 加速度資料起始位址（X 高位元組）
WHO_AM_I = 0x75      # 晶片身分，正版回 0x68；部分相容晶片回 0x70、0x72、0x98

# 量程 → (寫入值, 每 g 的原始數值)
RANGES = {2: (0x00, 16384), 4: (0x08, 8192), 8: (0x10, 4096), 16: (0x18, 2048)}


class MPU6050:
    def __init__(self, i2c, addr=ADDR, g_range=8, dlpf=None):
        self.i2c = i2c
        self.addr = addr
        if addr not in i2c.scan():
            raise OSError("找不到 MPU6050（位址 0x%02X），請檢查 SDA/SCL/VCC/GND 接線" % addr)
        self.i2c.writeto_mem(addr, PWR_MGMT_1, b"\x00")          # 喚醒
        cfg, self.lsb_per_g = RANGES[g_range]
        self.i2c.writeto_mem(addr, ACCEL_CONFIG, bytes([cfg]))    # 設定量程
        # 數位低通濾波（CONFIG 0x1A）：None＝不設定（晶片預設約 260 Hz）。
        # 若 50 Hz 取樣抓撞擊尖峰很不穩，試跑時可改 4（約 20 Hz），
        # 但 collect.py、main.py、Arduino 推論程式三者必須用同一個設定。
        if dlpf is not None:
            self.i2c.writeto_mem(addr, 0x1A, bytes([dlpf]))

    def who_am_i(self):
        return self.i2c.readfrom_mem(self.addr, WHO_AM_I, 1)[0]

    @staticmethod
    def _to_signed(hi, lo):
        v = (hi << 8) | lo
        return v - 65536 if v > 32767 else v

    def accel(self):
        """回傳 (ax, ay, az)，單位 g。靜止時總和約為 1 g。"""
        d = self.i2c.readfrom_mem(self.addr, ACCEL_XOUT_H, 6)
        s = self.lsb_per_g
        return (self._to_signed(d[0], d[1]) / s,
                self._to_signed(d[2], d[3]) / s,
                self._to_signed(d[4], d[5]) / s)
