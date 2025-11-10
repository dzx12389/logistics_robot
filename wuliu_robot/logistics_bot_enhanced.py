import hashlib
import base64
import requests
import json
import time
import re
from typing import Dict, Optional, List, Any


class LogisticsBot:
    def __init__(self):
        """
        初始化物流查询机器人
        """
        # ⚙️ 请替换为您自己的快递鸟凭证
        self.e_business_id = "1900914"
        self.api_key = "0455d8b7-c944-45f6-a86b-3f164f125f6f"

        self.query_history: List[Dict[str, Any]] = []
        self.base_url = "https://api.kdniao.com/Ebusiness/EbusinessOrderHandle.aspx"
        self.recognize_url = "https://api.kdniao.com/api/dist"
        self.timeout = 10

        # 状态码映射
        self.state_map = {
            '0': '无物流信息',
            '1': '已揽收',
            '2': '运输中',
            '3': '已签收',
            '4': '问题件'
        }

        # ✅ 官方快递公司编码
        self.shipper_map = {
            'SF': '顺丰速运',
            'YT': '圆通速递',
            'ZTO': '中通快递',
            'STO': '申通快递',
            'YD': '韵达快递',
            'HTKY': '百世快递',
            'JD': '京东物流',
            'EMS': 'EMS',
            'YZPY': '邮政快递包裹',
            'JTSD': '极兔速递',  # ✅ 官方正确编码
            'UC': '优速快递',
            'DBL': '德邦快递',
            'FAST': '快捷快递',
            'ZJS': '宅急送',
            'TNT': 'TNT快递',
            'UPS': 'UPS',
            'DHL': 'DHL',
            'FEDEX': '联邦快递'
        }

        # ✅ 识别规则支持 JT/JTO/JTSD 三种前缀
        self.shipper_rules = [
            {'code': 'SF', 'name': '顺丰速运', 'pattern': r'^SF\d{12,15}$'},
            {'code': 'YT', 'name': '圆通速递', 'pattern': r'^(YT|YTO)\d{12,15}$'},
            {'code': 'ZTO', 'name': '中通快递', 'pattern': r'^(ZTO|ZT)\d{12,15}$'},
            {'code': 'STO', 'name': '申通快递', 'pattern': r'^STO\d{12,15}$'},
            {'code': 'YD', 'name': '韵达快递', 'pattern': r'^(YD|YDA)\d{12,15}$'},
            {'code': 'HTKY', 'name': '百世快递', 'pattern': r'^(HTKY|BK)\d{12,15}$'},
            {'code': 'JD', 'name': '京东物流', 'pattern': r'^JD\d{12,15}$'},
            {'code': 'EMS', 'name': 'EMS', 'pattern': r'^[EJ]\d{13}CN$'},
            {'code': 'YZPY', 'name': '邮政快递包裹', 'pattern': r'^[A-Z]{2}\d{9}[A-Z]{2}$'},
            {'code': 'JTSD', 'name': '极兔速递', 'pattern': r'^(JT|JTSD|JTO)\d{12,15}$'},  # ✅ 三前缀识别
            {'code': 'DBL', 'name': '德邦快递', 'pattern': r'^DBL\d{12,15}$'},
            {'code': 'ZJS', 'name': '宅急送', 'pattern': r'^ZJS\d{12,15}$'},
            {'code': 'UPS', 'name': 'UPS', 'pattern': r'^1Z[A-Z0-9]{16}$'},
            {'code': 'DHL', 'name': 'DHL', 'pattern': r'^JJD\d{15}$'},
            {'code': 'FEDEX', 'name': '联邦快递', 'pattern': r'^96\d{12}$'}
        ]

    # 🔐 生成签名
    def generate_sign(self, data: str) -> str:
        sign_str = data + self.api_key
        sign_md5 = hashlib.md5(sign_str.encode()).hexdigest()
        return base64.b64encode(sign_md5.encode()).decode()

    # 🚚 模式识别
    def recognize_by_pattern(self, logistic_code: str) -> Optional[str]:
        try:
            cleaned_code = re.sub(r'[\s-]', '', logistic_code.upper())
            for rule in self.shipper_rules:
                if re.match(rule['pattern'], cleaned_code):
                    shipper_code = rule['code']
                    # ✅ 强制修正：极兔任何前缀都统一用 JTSD
                    if shipper_code in ["JTO", "JT"]:
                        shipper_code = "JTSD"
                    print(f"🔍 基于规则识别为：{rule['name']} ({shipper_code})")
                    return shipper_code
            return None
        except Exception as e:
            print(f"⚠️ 模式识别失败：{str(e)}")
            return None

    # 🔍 自动识别快递公司
    def auto_recognize_shipper(self, logistic_code: str) -> Optional[str]:
        try:
            print("\n🔍 正在尝试识别快递公司...")
            shipper_code = self.recognize_by_pattern(logistic_code)
            if shipper_code:
                return shipper_code

            payload = {
                "EBusinessID": self.e_business_id,
                "RequestType": "2002",
                "LogisticCode": logistic_code,
                "DataType": "2"
            }
            response = requests.post(self.recognize_url, data=payload, timeout=5)
            result = response.json()
            if result.get('Success') and result.get('Shippers'):
                shipper_info = result['Shippers'][0]
                code = shipper_info['ShipperCode']
                # ✅ 极兔接口识别为 JTO 时自动修正
                if code == "JTO":
                    code = "JTSD"
                print(f"✅ API识别成功：{shipper_info['ShipperName']} ({code})")
                return code

            return None
        except Exception as e:
            print(f"⚠️ 识别失败：{str(e)}")
            return None

    # 📦 查询物流信息
    def get_logistics_info(self, logistic_code: str, shipper_code: Optional[str] = None) -> Dict[str, Any]:
        if not shipper_code:
            shipper_code = self.auto_recognize_shipper(logistic_code)
            if not shipper_code:
                return {"Success": False, "Reason": "无法识别快递公司，请手动输入"}

        req_data = {
            "OrderCode": "",
            "ShipperCode": shipper_code,
            "LogisticCode": logistic_code
        }

        raw_data = json.dumps(req_data, separators=(',', ':'))
        data_sign = self.generate_sign(raw_data)

        # ✅ 优先使用新版接口 (8001)
        payload = {
            "EBusinessID": self.e_business_id,
            "RequestType": "8001",
            "RequestData": raw_data,
            "DataSign": data_sign,
            "DataType": "2"
        }

        try:
            response = requests.post(self.base_url, data=payload, timeout=self.timeout)
            result = response.json()

            # 自动回退到旧接口
            if not result.get('Success') and '没有可用套餐' in result.get('Reason', ''):
                print("⚠️ 检测到新接口无套餐，自动回退旧接口（1002）...")
                payload["RequestType"] = "1002"
                response = requests.post(self.base_url, data=payload, timeout=self.timeout)
                result = response.json()

            # 友好提示
            if not result.get('Success') and '没有可用套餐' in result.get('Reason', ''):
                result['Reason'] += " 👉 请在快递鸟控制台开通【快递查询】套餐。"

            # 保存查询历史
            self.query_history.append({
                'timestamp': time.time(),
                'datetime': time.strftime("%Y-%m-%d %H:%M:%S"),
                'logistic_code': logistic_code,
                'shipper_code': shipper_code,
                'shipper_name': self.shipper_map.get(shipper_code, shipper_code),
                'result': result
            })

            return result

        except Exception as e:
            return {"Success": False, "Reason": f"查询失败：{str(e)}"}

    # 🎨 格式化输出
    def format_logistics_response(self, result: Dict[str, Any]) -> str:
        if not result.get('Success'):
            return f"❌ 查询失败：{result.get('Reason', '未知错误')}"

        logistic_code = result.get('LogisticCode', '')
        shipper_code = result.get('ShipperCode', '')
        state = result.get('State', '')
        traces = result.get('Traces', [])

        response = f"\n📦 快递信息查询结果"
        response += f"\n{'=' * 50}"
        response += f"\n单号：{logistic_code}"
        response += f"\n快递公司：{self.shipper_map.get(shipper_code, shipper_code)}"
        response += f"\n当前状态：{self.state_map.get(state, state)}"

        if traces:
            response += "\n\n🚚 物流轨迹："
            for i, trace in enumerate(traces, 1):
                response += f"\n{i:2d}. {trace.get('AcceptTime', '')} - {trace.get('AcceptStation', '')}"

        return response

    # 🧾 历史查询
    def show_history(self, limit: int = 10) -> str:
        if not self.query_history:
            return "📜 暂无查询历史"
        response = f"\n📜 查询历史记录（最近{min(limit, len(self.query_history))}条）"
        response += f"\n{'=' * 60}"
        for i, record in enumerate(reversed(self.query_history[:limit]), 1):
            response += f"\n{i}. {record['datetime']} | {record['logistic_code']} | {record['shipper_name']}"
        return response

    # 🧠 运行交互模式
    def run(self):
        print("=" * 60)
        print("📦 欢迎使用快递查询机器人 v2.3（极兔修正版）")
        print("💡 功能说明：")
        print("   - 输入快递单号直接查询物流信息")
        print("   - 自动识别快递公司（含极兔JTSD自动纠正）")
        print("   - 输入 'history' 查看历史记录")
        print("   - 输入 'exit' 退出程序")
        print("=" * 60)

        while True:
            user_input = input("\n请输入快递单号：").strip()
            if user_input.lower() == "exit":
                print("\n👋 感谢使用，再见！")
                break
            elif user_input.lower() == "history":
                print(self.show_history())
                continue
            elif not user_input:
                print("⚠️ 请输入有效单号")
                continue

            print(f"\n🔍 正在查询单号 {user_input}...")
            result = self.get_logistics_info(user_input)
            print(self.format_logistics_response(result))


def main():
    bot = LogisticsBot()
    bot.run()


if __name__ == "__main__":
    main()
