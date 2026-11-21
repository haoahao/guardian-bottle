# Python 實作：單一模組 → 雙模組 → 課堂測驗

先把 `micropython/` 裡的 `mpu6050.py`、`guardian.py` 存進 Pico W，用到 MPU6050 的程式才找得到它們。

## 範例 examples/（老師帶著做）

| 檔案 | 模組 | 生活情境 |
| --- | --- | --- |
| e01_bike_light.py | LED | 腳踏車尾燈 |
| e02_breathing.py | LED（PWM） | 手機呼吸通知燈 |
| e03_microwave.py | 蜂鳴器 | 微波爐叮叮叮 |
| e04_doorbell.py | 蜂鳴器 | 門鈴叮咚 |
| e05_mpu_test.py | MPU6050 | 手機怎麼知道你轉螢幕 |
| e06_thermometer.py | Pico W 內建溫度感測器 | 教室溫度計 |
| e07_oven_timer.py | LED＋蜂鳴器 | 烤箱倒數計時器 |
| e08_level.py | MPU6050＋LED | 水平儀 |
| e09_anti_theft.py | MPU6050＋蜂鳴器 | 機車防盜器 |
| e10_overheat.py | 溫度＋LED | 電暖器過熱警示 |

## 課堂測驗 quiz/（自己寫）

每個檔案開頭有情境、要求和提示，把 `# TODO` 的地方寫完。

| 檔案 | 模組 | 題目 |
| --- | --- | --- |
| q01_sos.py | LED | 求救燈 SOS |
| q02_dimmer.py | LED | 檯燈五段調光 |
| q03_scale.py | 蜂鳴器 | 音樂盒音階 |
| q04_parking.py | 蜂鳴器 | 倒車雷達 |
| q05_pose.py | MPU6050 | 智慧手環判斷姿勢 |
| q06_temp_stats.py | 溫度 | 氣象站每日統計 |
| q07_crosswalk.py | LED＋蜂鳴器 | 行人號誌倒數 |
| q08_tilt_dimmer.py | MPU6050＋LED | 傾斜感應夜燈 |
| q09_tilt_music.py | MPU6050＋蜂鳴器 | 體感電子樂器 |
| q10_pedometer.py | MPU6050＋LED | 計步器 |
