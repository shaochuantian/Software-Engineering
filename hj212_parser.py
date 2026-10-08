class HJ212Parser:
    def __init__(self):
        self.crc_init = 0xFFFF
        self.crc_poly = 0xA001

    def is_valid_message(self, message):
        """检查报文格式是否正确 (## + 4位长度 + 数据段 + 4位CRC + \r\n)"""
        if not message.startswith("##") or not message.endswith("\r\n"):
            return False
        if len(message) < 12: # 最短长度校验
            return False
        return True

    def validate_crc(self, message):
        """实现ANSI CRC16算法，校验报文的CRC值"""
        # 提取需要校验的部分 (数据段) 和 报文自带的CRC
        try:
            data_length = int(message[2:6])
            data_segment = message[6:6+data_length]
            expected_crc = message[6+data_length:6+data_length+4]
            
            # 计算 CRC16
            crc = self.crc_init
            for char in data_segment:
                crc ^= ord(char)
                for _ in range(8):
                    if crc & 1:
                        crc = (crc >> 1) ^ self.crc_poly
                    else:
                        crc >>= 1
            # 将计算得到的CRC转为4位大写十六进制字符串
            calculated_crc = f"{crc:04X}"
            return calculated_crc == expected_crc
        except Exception:
            return False

    def parse_data_segment(self, message):
        """解析数据段，返回包含所有键值对的字典"""
        try:
            data_length = int(message[2:6])
            data_segment = message[6:6+data_length]
            
            result = {}
            # 数据段以 && 分隔不同的部分，但简单起见我们按 ; 分割键值对
            parts = data_segment.replace("&&", ";").split(';')
            for part in parts:
                if '=' in part:
                    key, value = part.split('=', 1)
                    result[key] = value
            return result
        except Exception:
            return {}

    def extract_monitoring_data(self, message):
        """从CP字段中提取所有监测因子及其数值"""
        data_dict = self.parse_data_segment(message)
        cp_data = data_dict.get('CP', '')
        
        monitoring_data = {}
        if cp_data:
            # CP数据段内部可能用 , 分隔不同的监测因子指标
            factors = cp_data.split(',')
            for factor in factors:
                if '=' in factor:
                    k, v = factor.split('=', 1)
                    monitoring_data[k] = v
        return monitoring_data

# 简单测试代码
if __name__ == "__main__":
    # 这是一个模拟的HJ212报文用于测试运行结果
    test_msg = "##0024QN=20231008;CP=&&a01001-Rtd=15.2,a01002-Rtd=20.5&&7B2A\r\n"
    parser = HJ212Parser()
    print("格式校验:", parser.is_valid_message(test_msg))
    print("数据解析:", parser.parse_data_segment(test_msg))