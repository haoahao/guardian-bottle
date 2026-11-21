# Q03【單一模組｜蜂鳴器】音樂盒音階
# 生活情境：音樂盒從 Do 彈到高音 Do，再彈回來。
# 要求：
#   1. 頻率：Do 262、Re 294、Mi 330、Fa 349、Sol 392、La 440、Si 494、高 Do 523
#   2. 先往上彈，再往下彈（不重複高 Do）
#   3. 每個音 0.25 秒
# 提示：串列反過來可以用 notes[::-1]，去掉第一個用 [1:]。
# 接線：蜂鳴器模組 S → GP14、VCC → 3V3、GND → GND

from machine import Pin, PWM
import time

buzzer = PWM(Pin(14))
notes = [262, 294, 330, 349, 392, 440, 494, 523]

# TODO 1：寫 play(f)：響 0.25 秒再靜音

# TODO 2：往上彈、再往下彈
