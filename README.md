# 守護瓶任務｜樹莓派 AIoT 實作

臺北市立西松高中 115-1 週六微課程。用 Raspberry Pi Pico W 加上 MPU6050 加速度感測器，做一個「瓶子跌倒會警報」的守護瓶：第一週人寫規則，第二週錄資料訓練 AI，第三週規則和 AI 比賽。

## 檔案在哪裡

| 資料夾／檔案 | 內容 | 哪一週用 |
| --- | --- | --- |
| `python_basics/` | 5 個 Python 小程式：print、迴圈、LED、蜂鳴器、if、讀感測器 | 第一週 |
| `python_practice/` | 10 個範例（單一模組→雙模組生活情境）＋10 題課堂測驗 | 第一週 |
| `micropython/main.py` | 守護瓶主程式：`STEP = 1` 看數字、`STEP = 2` 規則判斷 | 第一週 |
| `micropython/guardian.py` | 共用工具：總加速度、傾斜角、站立校準 | 第一週起 |
| `micropython/mpu6050.py`、`ssd1306.py` | 感測器和 OLED 的驅動程式 | 第一週起 |
| `micropython/collect.py` | 錄資料用（存成 CSV） | 第二週 |
| `thresholds.md` | 各組定出的門檻紀錄 | 每一週 |

## 怎麼下載

按右上方綠色的 **Code** → **Download ZIP**，解壓縮到桌面。

## 怎麼存進 Pico W

1. Pico W 用 USB 接電腦，打開 Thonny，右下角選 **MicroPython (Raspberry Pi Pico)**。
2. 打開 `micropython/` 裡的每一個 `.py` 檔，按 **檔案 → 另存新檔 → Raspberry Pi Pico**，檔名不要改。
3. 5 個檔都存好後，在板子上打開 `main.py` 按 F5 執行。

`python_basics/` 的前 4 個程式不用存進板子，在 Thonny 打開直接按 F5 就能跑。

## 接線

| 元件 | 接到 Pico W |
| --- | --- |
| MPU6050 | VCC→3V3、GND→GND、SDA→GP4、SCL→GP5（用 40 cm 公對母杜邦線） |
| OLED（2.42 吋，第二週才接） | GND→GND、VDD→3V3、SCL→GP5、SDA→GP4（和 MPU6050 共用 I2C；要先焊排針、短接背面 D2） |
| LED | GP15 → 220Ω → LED 長腳，短腳→GND |
| 無源蜂鳴器模組（Keyes，3 支腳） | S→GP14、VCC→3V3、GND→GND（VCC 一定要接，板上電晶體靠它推喇叭） |

第一週沒接 OLED，I2C 掃描看到 `0x68`（MPU6050）就成功；第二週接上 OLED 後會看到 `0x3c` 和 `0x68`。沒接 OLED 時 `main.py` 照常執行，數字只顯示在 Shell。

## 什麼是 commit

每一次修改檔案並按下「Commit」，GitHub 就會留下一筆紀錄：誰、什麼時候、改了哪幾行。點檔案右上角的時鐘圖示可以看到所有歷史，就像遊戲的存檔點，隨時可以回頭比較。
