# -*- coding: utf-8 -*-
"""
实验四 B1：恒温水箱 (20°C ~ 100°C) 状态机实现
状态说明：
- IDLE: 准备/待机检测状态（启动后检测温度、水量、时间与电路）
- HEATING: 加热状态（温度 < 20°C 且有水时打开继电器加热，达到 100°C 断开电源）
- NO_WATER_WAIT: 缺水待机状态（温度 < 20°C 但无水，不开电源，等待加水）
- SLEEP: 休眠状态（晚上 23:00 自动断开电源进入休眠，早上 07:00 自动恢复恒温烧水）
- REPAIR: 维修状态（水箱烧坏/故障时断开电源并进入维修）
"""

from enum import Enum


class TankState(Enum):
    IDLE = "准备/待机状态"
    HEATING = "加热状态"
    NO_WATER_WAIT = "缺水待机状态"
    SLEEP = "休眠状态"
    REPAIR = "维修状态"


class WaterTankStateMachine:
    def __init__(self):
        self.state = TankState.IDLE
        self.relay_on = False
        self.temperature = 25.0
        self.has_water = True
        self.hour = 8
        self.is_broken = False

    def _set_relay(self, on: bool):
        if self.relay_on != on:
            self.relay_on = on
            action = "打开继电器电源，开始烧水" if on else "断开继电器电源"
            print(f"  [动作] {action}")

    def step(self, temperature: float = None, has_water: bool = None,
             hour: int = None, is_broken: bool = None):
        if temperature is not None:
            self.temperature = temperature
        if has_water is not None:
            self.has_water = has_water
        if hour is not None:
            self.hour = hour
        if is_broken is not None:
            self.is_broken = is_broken

        print(f"[输入] 时间={self.hour:02d}:00, 温度={self.temperature}°C, "
              f"有水={self.has_water}, 故障={self.is_broken} | 当前状态: {self.state.value}")

        # 最高优先级：水箱烧坏 -> 进入维修状态
        if self.is_broken and self.state != TankState.REPAIR:
            self._set_relay(False)
            self.state = TankState.REPAIR
            print(f"  [状态转移] -> {self.state.value}（水箱烧坏，等待维修）")
            return

        # 维修状态下，若故障未排除则保持维修；若已修好则回到准备状态
        if self.state == TankState.REPAIR:
            if not self.is_broken:
                self.state = TankState.IDLE
                print(f"  [状态转移] -> {self.state.value}（维修完成，恢复运行）")
            else:
                return

        # 定时规则：晚上 23:00 断开电源进入休眠
        if self.hour == 23 and self.state != TankState.SLEEP:
            self._set_relay(False)
            self.state = TankState.SLEEP
            print(f"  [状态转移] -> {self.state.value}（晚上11点整，自动休眠）")
            return

        # 休眠状态处理：早上 07:00 自动唤醒进入恒温烧水检测
        if self.state == TankState.SLEEP:
            if self.hour == 7:
                self.state = TankState.IDLE
                print(f"  [状态转移] -> {self.state.value}（早上7点整，自动唤醒）")
            else:
                return

        # 正常工作状态下的温控与水量逻辑
        if self.state in (TankState.IDLE, TankState.NO_WATER_WAIT):
            if self.temperature < 20.0:
                if self.has_water:
                    self.state = TankState.HEATING
                    self._set_relay(True)
                    print(f"  [状态转移] -> {self.state.value}")
                else:
                    if self.state != TankState.NO_WATER_WAIT:
                        self.state = TankState.NO_WATER_WAIT
                        self._set_relay(False)
                        print(f"  [状态转移] -> {self.state.value}（温度低于20°C但无水，不开启电源）")
        elif self.state == TankState.HEATING:
            if not self.has_water:
                self.state = TankState.NO_WATER_WAIT
                self._set_relay(False)
                print(f"  [状态转移] -> {self.state.value}（加热中缺水，紧急断电）")
            elif self.temperature >= 100.0:
                self.state = TankState.IDLE
                self._set_relay(False)
                print(f"  [状态转移] -> {self.state.value}（水温达到100°C，断开电源）")


if __name__ == "__main__":
    print("=== B1 恒温水箱状态机测试 ===")
    tank = WaterTankStateMachine()
    tank.step(temperature=18.0, has_water=False, hour=8)   # 低于20°C但无水 -> 不开电源
    tank.step(temperature=18.0, has_water=True, hour=8)    # 加水后 -> 开始加热
    tank.step(temperature=65.0, has_water=True, hour=9)    # 持续加热
    tank.step(temperature=100.0, has_water=True, hour=9)   # 达到100°C -> 断开电源
    tank.step(temperature=19.0, has_water=True, hour=23)   # 晚上23点 -> 进入休眠
    tank.step(temperature=15.0, has_water=True, hour=7)    # 早上7点 -> 唤醒并低于20°C有水开始加热
    tank.step(temperature=50.0, has_water=True, hour=10, is_broken=True)   # 烧坏 -> 进入维修
    tank.step(temperature=50.0, has_water=True, hour=10, is_broken=False)  # 修好 -> 恢复准备状态
