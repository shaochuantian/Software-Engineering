# -*- coding: utf-8 -*-
"""
实验四 B2：SafeHome 控制面板 (ControlPanel) 状态机实现
状态与规则说明：
- STANDBY: 待机状态（等待户主敲击按键）
- READING_KEYS: 读取键入字符状态（每输入1个字符累计长度，达到4位验证密码）
- LOCKED: 锁定状态（密码连续错误3次后锁定，锁定超过120秒后恢复待机允许再次输入）
- FUNCTION_SELECT: 系统功能选择状态（密码正确后进入）
"""

from enum import Enum


class PanelState(Enum):
    STANDBY = "待机状态"
    READING_KEYS = "读取键入字符状态"
    LOCKED = "锁定状态"
    FUNCTION_SELECT = "系统功能选择状态"


class SafeHomeControlPanel:
    def __init__(self, correct_password: str = "1234", max_attempts: int = 3, lock_duration: int = 120):
        if len(correct_password) != 4 or not correct_password.isdigit():
            raise ValueError("设置密码必须为4位数字")
        self.correct_password = correct_password
        self.max_attempts = max_attempts
        self.lock_duration = lock_duration

        self.state = PanelState.STANDBY
        self.input_buffer = ""
        self.error_count = 0
        self.locked_elapsed = 0

    def press_key(self, key: str):
        """模拟户主敲击控制面板键盘按键"""
        if self.state == PanelState.LOCKED:
            print(f"[拒绝按键 '{key}'] 当前处于{self.state.value}（已锁定 {self.locked_elapsed}s / 需超过 {self.lock_duration}s）")
            return

        if self.state == PanelState.FUNCTION_SELECT:
            print(f"[系统功能选择] 当前已解锁，执行功能指令: '{key}'")
            return

        # 从待机进入读取键入字符状态
        if self.state == PanelState.STANDBY:
            self.state = PanelState.READING_KEYS
            print(f"[状态转移] 待机状态 -> {self.state.value}")

        self.input_buffer += key
        print(f"  [按键输入] 键入 '{key}'，当前输入长度: {len(self.input_buffer)}/4")

        # 比较输入密码长度是否达到 4 位
        if len(self.input_buffer) == 4:
            self._verify_password()

    def _verify_password(self):
        if self.input_buffer == self.correct_password:
            self.error_count = 0
            self.input_buffer = ""
            self.state = PanelState.FUNCTION_SELECT
            print(f"  [验证通过] 密码正确！状态转移 -> {self.state.value}")
        else:
            self.error_count += 1
            wrong_pwd = self.input_buffer
            self.input_buffer = ""
            print(f"  [验证失败] 输入 '{wrong_pwd}' 错误（累计错误 {self.error_count}/{self.max_attempts} 次）")

            if self.error_count >= self.max_attempts:
                self.state = PanelState.LOCKED
                self.locked_elapsed = 0
                print(f"  [状态转移] 错误达到3次 -> {self.state.value}（锁定控制面板）")
            else:
                self.state = PanelState.STANDBY
                print(f"  [状态转移] 未达3次 -> 返回{self.state.value}，请重新输入")

    def tick(self, seconds: int):
        """模拟时间流逝（秒）"""
        if self.state == PanelState.LOCKED:
            self.locked_elapsed += seconds
            print(f"[时间推进] 锁定计时 +{seconds}s，累计锁定 {self.locked_elapsed}s")
            if self.locked_elapsed > self.lock_duration:
                self.state = PanelState.STANDBY
                self.error_count = 0
                self.locked_elapsed = 0
                print(f"  [状态转移] 锁定时间超过120秒 -> {self.state.value}，允许户主重新输入")


if __name__ == "__main__":
    print("=== B2 SafeHome 控制面板状态机测试 ===")
    panel = SafeHomeControlPanel(correct_password="2580")

    # 连续输错 3 次密码
    for attempt in ["1111", "2222", "3333"]:
        for ch in attempt:
            panel.press_key(ch)

    # 锁定期间按键无效
    panel.press_key("2")

    # 时间经过 121 秒（超过 120 秒）
    panel.tick(121)

    # 输入正确密码 2580
    for ch in "2580":
        panel.press_key(ch)
