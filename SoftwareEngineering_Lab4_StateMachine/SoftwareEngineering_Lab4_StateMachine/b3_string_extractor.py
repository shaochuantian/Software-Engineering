# -*- coding: utf-8 -*-
"""
实验四 B3：源代码字符串提取器（基于有限状态机 FSM）
状态说明：
- IDLE: 空闲/代码扫描状态（遇到双引号 '"' 进入 IN_STRING 状态，忽略其他字符）
- IN_STRING: 字符串内状态（收集字符；遇到反斜杠 '\\' 进入 ESCAPE 状态；遇到未转义双引号 '"' 输出字符串并返回 IDLE）
- ESCAPE: 转义状态（将紧随反斜杠后的字符按转义规则追加到当前字符串缓存，随后返回 IN_STRING）
"""

from enum import Enum
from typing import List


class ExtractorState(Enum):
    IDLE = "空闲状态"
    IN_STRING = "字符串内状态"
    ESCAPE = "转义状态"


class StringExtractorFSM:
    def __init__(self, verbose: bool = False):
        self.state = ExtractorState.IDLE
        self.current_chars: List[str] = []
        self.extracted_strings: List[str] = []
        self.verbose = verbose

    def _log(self, msg: str):
        if self.verbose:
            print(msg)

    def extract(self, source_code: str) -> List[str]:
        self.state = ExtractorState.IDLE
        self.current_chars = []
        self.extracted_strings = []

        for idx, ch in enumerate(source_code):
            if self.state == ExtractorState.IDLE:
                if ch == '"':
                    self.state = ExtractorState.IN_STRING
                    self.current_chars = []
                    self._log(f"[{idx}] 读到 '\"' : IDLE -> IN_STRING")
            elif self.state == ExtractorState.IN_STRING:
                if ch == '\\':
                    self.state = ExtractorState.ESCAPE
                    self._log(f"[{idx}] 读到 '\\' : IN_STRING -> ESCAPE")
                elif ch == '"':
                    result = "".join(self.current_chars)
                    self.extracted_strings.append(result)
                    self.current_chars = []
                    self.state = ExtractorState.IDLE
                    self._log(f"[{idx}] 读到 '\"' : IN_STRING -> IDLE | 提取结果: {result}")
                else:
                    self.current_chars.append(ch)
            elif self.state == ExtractorState.ESCAPE:
                escape_map = {
                    '"': '"',
                    '\\': '\\',
                    'n': '\n',
                    't': '\t',
                    'r': '\r',
                }
                self.current_chars.append(escape_map.get(ch, ch))
                self.state = ExtractorState.IN_STRING
                self._log(f"[{idx}] 转义字符 '{ch}' : ESCAPE -> IN_STRING")

        return self.extracted_strings


if __name__ == "__main__":
    print("=== B3 源代码字符串提取状态机测试 ===")
    sample_code = (
        '#include <stdio.h>\n'
        'int main() {\n'
        '    const char* msg1 = "一般学习一门编程语言的时候，基本上第一个程序是输出\\"Hello World!\\"";\n'
        '    const char* msg2 = "路径示例: C:\\\\Users\\\\Admin\\\\test.py";\n'
        '    printf("%s\\n", msg1);\n'
        '    return 0;\n'
        '}'
    )

    fsm = StringExtractorFSM(verbose=True)
    strings = fsm.extract(sample_code)

    print("\n--- 最终提取到的所有字符串 ---")
    for i, s in enumerate(strings, 1):
        print(f"{i}. {s}")
