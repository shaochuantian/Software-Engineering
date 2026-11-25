# 软件工程实验四：面向对象的系统建模B（状态机 Python 实现）

## 目录结构
- `b1_water_tank.py`：B1 恒温水箱（20°C~100°C）状态机实现（含缺水检测、100°C断电、故障维修、23:00休眠与07:00唤醒）。
- `b2_safehome_panel.py`：B2 SafeHome 控制面板（ControlPanel）状态机实现（含4位密码长度校验、3次错误锁定、超过120秒自动解锁）。
- `b3_string_extractor.py`：B3 源代码字符串提取器状态机实现（支持双引号匹配与反斜杠转义字符解析）。

## 运行方式
确保本地已安装 Python 3.8+，在当前文件夹下直接运行对应脚本即可查看状态转移过程与测试用例输出：

```bash
python b1_water_tank.py
python b2_safehome_panel.py
python b3_string_extractor.py
```
