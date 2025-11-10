import hashlib
import base64
import requests
import json
import time
from typing import Dict, Optional, List, Any

class LogisticsBot:
    def __init__(self):
        """
        初始化物流查询机器人
        """
        # TODO: 请替换为您自己的快递鸟凭证
        self.e_business_id = "你的商户ID"
        self.api_key = "你的快递鸟API密钥"
        
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
        
        # 快递公司编码映射
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
            'JTO': '极兔速递',
            'UC': '优速快递',
            'DBL': '德邦快递',
            'FAST': '快捷快递',
            'ZJS': '宅急送',
            'TNT': 'TNT快递',
            'UPS': 'UPS',
            'DHL': 'DHL',
            'FEDEX': '联邦快递'
        }

    def generate_sign(self, data: str) -> str:
        """
        生成签名
        
        Args:
            data: 待签名的数据字符串
            
        Returns:
            签名结果
        """
        sign_str = data + self.api_key
        sign_md5 = hashlib.md5(sign_str.encode()).hexdigest()
        return base64.b64encode(sign_md5.encode()).decode()

    def auto_recognize_shipper(self, logistic_code: str) -> Optional[str]:
        """
        自动识别快递公司
        
        Args:
            logistic_code: 快递单号
            
        Returns:
            快递公司编码或None
        """
        try:
            payload = {
                "EBusinessID": self.e_business_id,
                "RequestType": "2002",  # 单号识别接口指令
                "LogisticCode": logistic_code,
                "DataType": "2"
            }
            
            response = requests.post(self.recognize_url, data=payload, timeout=5)
            result = response.json()
            
            if result.get('Success') and result.get('Shippers'):
                return result['Shippers'][0]['ShipperCode']
            return None
        except Exception as e:
            print(f"⚠️  自动识别快递公司失败：{str(e)}")
            return None

    def get_logistics_info(self, logistic_code: str, shipper_code: Optional[str] = None) -> Dict[str, Any]:
        """
        查询物流信息
        
        Args:
            logistic_code: 快递单号
            shipper_code: 快递公司编码（可选，自动识别）
            
        Returns:
            查询结果字典
        """
        # 如果没有提供快递公司编码，自动识别
        if not shipper_code:
            shipper_code = self.auto_recognize_shipper(logistic_code)
            if not shipper_code:
                return {"Success": False, "Reason": "无法识别快递公司，请手动输入"}
        
        # 构造请求数据
        req_data = {
            "OrderCode": "",
            "ShipperCode": shipper_code,
            "LogisticCode": logistic_code
        }
        
        try:
            # 生成签名
            raw_data = json.dumps(req_data, separators=(',', ':'))
            data_sign = self.generate_sign(raw_data)
            
            # 构造请求参数
            payload = {
                "EBusinessID": self.e_business_id,
                "RequestType": "1002",  # 即时查询接口指令
                "RequestData": raw_data,
                "DataSign": data_sign,
                "DataType": "2"
            }
            
            # 发送请求
            response = requests.post(self.base_url, data=payload, timeout=self.timeout)
            result = response.json()
            
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
            error_msg = f"查询失败：{str(e)}"
            print(f"❌ {error_msg}")
            return {"Success": False, "Reason": error_msg}

    def format_logistics_response(self, result: Dict[str, Any]) -> str:
        """
        格式化物流查询结果
        
        Args:
            result: 查询结果字典
            
        Returns:
            格式化的字符串
        """
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
            latest_trace = traces[0]
            response += f"\n最新更新：{latest_trace.get('AcceptTime', '')}"
            response += f"\n当前位置：{latest_trace.get('Location', '')}"
            
            response += "\n\n🚚 物流轨迹："
            for i, trace in enumerate(traces, 1):
                time_str = trace.get('AcceptTime', '')
                station = trace.get('AcceptStation', '')
                response += f"\n{i:2d}. {time_str} - {station}"
        
        return response

    def show_supported_shippers(self):
        """
        显示支持的快递公司编码
        """
        print("\n📦 支持的快递公司编码：")
        print("-" * 40)
        
        # 按快递公司名称排序
        sorted_shippers = sorted(self.shipper_map.items(), key=lambda x: x[1])
        
        # 每行显示3个
        for i, (code, name) in enumerate(sorted_shippers, 1):
            print(f"{code:<10} {name:<15}", end="")
            if i % 3 == 0:
                print()
        if len(sorted_shippers) % 3 != 0:
            print()
        print("-" * 40)
        print("使用方法：输入快递单号后，如系统无法识别，可手动输入对应编码")

    def show_history(self, limit: int = 10) -> str:
        """
        显示查询历史
        
        Args:
            limit: 显示条数限制
            
        Returns:
            历史记录字符串
        """
        if not self.query_history:
            return "📜 暂无查询历史"
        
        response = f"\n📜 查询历史记录（最近{min(limit, len(self.query_history))}条）"
        response += f"\n{'=' * 50}"
        
        for i, record in enumerate(reversed(self.query_history[:limit]), 1):
            response += f"\n{i}. {record['datetime']} | {record['logistic_code']} | {record['shipper_name']}"
        
        return response

    def run(self):
        """
        运行交互式物流查询机器人
        """
        # 验证凭证是否填写
        if self.e_business_id == "你的商户ID" or self.api_key == "你的APIKey":
            print("❌ 请先配置你的快递鸟凭证！")
            print("   1. 打开 logistics_bot_standalone.py 文件")
            print("   2. 找到 __init__ 方法中的 e_business_id 和 api_key")
            print("   3. 替换为你自己的快递鸟凭证")
            print("   4. 保存文件并重新运行程序")
            return
        
        print("=" * 60)
        print("📦 欢迎使用快递查询机器人 v1.0")
        print("💡 功能说明：")
        print("   - 输入快递单号直接查询物流信息")
        print("   - 输入 'history' 查看查询历史")
        print("   - 输入 'exit' 退出程序")
        print("   - 输入 'help' 查看支持的快递公司编码")
        print("=" * 60)
        
        while True:
            try:
                user_input = input("\n请输入快递单号：").strip()
                
                if user_input.lower() == 'exit':
                    print("\n👋 感谢使用，再见！")
                    break
                
                elif user_input.lower() == 'history':
                    print(self.show_history())
                    continue
                
                elif user_input.lower() == 'help':
                    self.show_supported_shippers()
                    continue
                
                elif not user_input:
                    print("⚠️  请输入有效的快递单号")
                    continue
                
                # 显示加载动画
                print(f"\n🔍 正在查询单号 {user_input}...", end="")
                for _ in range(3):
                    print(".", end="", flush=True)
                    time.sleep(0.5)
                
                # 查询物流信息（先尝试自动识别）
                result = self.get_logistics_info(user_input)
                
                # 如果无法识别快递公司，让用户手动输入
                if not result.get('Success') and "无法识别快递公司" in result.get('Reason', ''):
                    print("\n")  # 换行
                    print("❓ 系统无法自动识别该快递公司")
                    print("   输入 'help' 查看支持的快递公司编码")
                    shipper_code = input("请输入快递公司编码：").strip().upper()
                    
                    if shipper_code == 'HELP':
                        self.show_supported_shippers()
                        shipper_code = input("请输入快递公司编码：").strip().upper()
                    
                    if shipper_code in self.shipper_map:
                        print(f"\n🔍 使用手动输入的 {self.shipper_map[shipper_code]} 重新查询...", end="")
                        for _ in range(3):
                            print(".", end="", flush=True)
                            time.sleep(0.3)
                        result = self.get_logistics_info(user_input, shipper_code)
                    else:
                        result = {"Success": False, "Reason": f"不支持的快递公司编码：{shipper_code}"}
                
                # 显示结果
                print(self.format_logistics_response(result))
                
            except KeyboardInterrupt:
                print("\n\n👋 用户中断，再见！")
                break
            except Exception as e:
                print(f"\n❌ 程序出错：{str(e)}")

def main():
    """
    主函数：初始化并运行机器人
    """
    try:
        # 创建机器人实例
        bot = LogisticsBot()
        
        # 运行机器人
        bot.run()
        
    except Exception as e:
        print(f"❌ 程序启动失败：{str(e)}")

if __name__ == "__main__":
    main()
