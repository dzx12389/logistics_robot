# robot.py - 物流机器人主类
import sys
import os
# 确保当前目录在搜索路径中，解决模块导入问题
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data import LOGISTICS_DATA
from smart_ai_router import SmartAIRouter
from utils import extract_tracking_number, format_tracking_response

class LogisticsRobot:
    def __init__(self):
        self.logistics_data = LOGISTICS_DATA  # 加载本地物流数据
        self.ai_router = SmartAIRouter()  # 初始化AI路由（包含智谱AI和本地备份）
        print("🤖 物流助手已启动（智谱AI增强版）")

    def query_logistics(self, tracking_number):
        """查询物流信息：优先使用本地数据，本地无数据则调用智谱AI"""
        tracking_number = tracking_number.upper()  # 统一转为大写，避免大小写问题
        if tracking_number in self.logistics_data:
            # 本地有数据，格式化后返回
            return format_tracking_response(self.logistics_data[tracking_number], tracking_number)
        else:
            # 本地无数据，调用智谱AI处理
            return self.ai_router.get_ai_response(f"运单号{tracking_number}不存在或未查询到信息，该如何处理？")

    def chat(self):
        """主聊天循环：处理用户输入，分发本地查询或AI调用"""
        print("=" * 50)
        print("🚚 智能物流助手（智谱AI驱动）")
        print("💡 功能：查询快递状态、咨询运费/时效/包装等")
        print("💡 提示：输入运单号直接查询，输入'退出'结束对话")
        print("=" * 50)

        while True:
            try:
                user_input = input("\n👤 您: ").strip()
                
                # 处理退出指令
                if user_input.lower() in ["退出", "再见", "bye", "拜拜"]:
                    print("🤖 助手: 感谢使用！再见啦~ 👋")
                    break
                
                # 忽略空输入
                if not user_input:
                    continue
                
                # 提取运单号（仅已知运单会被识别，避免误判）
                tracking_number = extract_tracking_number(user_input)
                if tracking_number:
                    # 运单号存在，使用本地数据查询
                    response = self.query_logistics(tracking_number)
                    print(f"🤖 助手(本地数据): {response}")
                else:
                    # 非运单问题，调用智谱AI
                    response = self.ai_router.get_ai_response(user_input)
                    print(f"🤖 助手(智谱AI): {response}")
                
            except KeyboardInterrupt:
                # 处理Ctrl+C强制退出
                print("\n🤖 助手: 已强制退出，再见！")
                break
            except Exception as e:
                # 捕获其他异常，避免程序崩溃
                print(f"🤖 助手: 出现错误：{str(e)}，请重试~")

# 测试代码
if __name__ == "__main__":
    robot = LogisticsRobot()
    print("✅ LogisticsRobot 类创建成功")