import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from logistics_bot_enhanced import LogisticsBot  # 快递鸟真实物流查询
from smart_ai_router import SmartAIRouter        # 智谱AI智能回复
from utils import extract_tracking_number, classify_intent  # 工具函数

class SmartRealLogisticsBot:
    def __init__(self):
        # 初始化两大核心模块
        self.logistics_bot = LogisticsBot()  # 快递鸟实例（需先配置凭证）
        self.ai_router = SmartAIRouter()     # 智谱AI实例（需配置APIKey）
        print("🤖 智能真实物流机器人已启动！")
        print("💡 支持：输入单号查真实物流、咨询运费/时效/包装等问题")

    def handle_user_input(self, user_input):
        """统一处理用户输入：分流物流查询/智能咨询"""
        user_input = user_input.strip()
        if not user_input:
            return "⚠️ 请输入有效内容（快递单号或物流相关问题）"
        
        # 步骤1：提取快递单号（优先处理物流查询需求）
        tracking_number = extract_tracking_number(user_input)
        # 步骤2：分类用户意图
        intent = classify_intent(user_input)

        # 场景1：纯物流查询（有单号+意图为物流查询）
        if tracking_number and intent == "物流查询":
            try:
                # 调用快递鸟查真实物流
                logistics_result = self.logistics_bot.get_logistics_info(tracking_number)
                formatted_logistics = self.logistics_bot.format_logistics_response(logistics_result)
                # 若查询成功，AI补充友好提示；失败则AI解释原因
                if logistics_result.get("Success"):
                    ai_tip = self.ai_router.get_ai_response(f"用户查询了单号{tracking_number}的物流，补充一句友好提示")
                    return f"{formatted_logistics}\n\n{ai_tip}"
                else:
                    ai_explain = self.ai_router.get_ai_response(f"物流查询失败，原因是：{logistics_result.get('Reason')}，请友好告知用户并给出建议")
                    return f"{formatted_logistics}\n\n{ai_explain}"
            except Exception as e:
                return self.ai_router.get_ai_response(f"查询物流时出错：{str(e)}，请告知用户解决方案")
        
        # 场景2：混合需求（有单号+非物流查询，如“SF123多久到”）
        elif tracking_number and intent != "物流查询":
            # 先查物流，再用AI解答具体问题
            logistics_result = self.logistics_bot.get_logistics_info(tracking_number)
            formatted_logistics = self.logistics_bot.format_logistics_response(logistics_result)
            # 让AI结合物流结果解答问题
            ai_answer = self.ai_router.get_ai_response(f"用户的问题是：{user_input}，对应的物流查询结果是：{logistics_result}，请结合结果解答")
            return f"{formatted_logistics}\n\n🤖 智能解答：{ai_answer}"
        
        # 场景3：纯智能咨询（无单号，如“运费怎么算”）
        else:
            return self.ai_router.get_ai_response(user_input)

    def run(self):
        """交互式运行"""
        print("=" * 60)
        print("📦 智能真实物流机器人 v1.0")
        print("💡 操作说明：")
        print("   - 输入快递单号 → 查询真实物流轨迹")
        print("   - 输入问题（如运费/时效/包装） → 智能解答")
        print("   - 输入 'history' → 查看查询历史")
        print("   - 输入 'exit' → 退出程序")
        print("=" * 60)
        
        while True:
            try:
                user_input = input("\n👤 您: ").strip()
                if user_input.lower() == "exit":
                    print("🤖 再见！祝您生活愉快～ 👋")
                    break
                elif user_input.lower() == "history":
                    # 显示快递鸟查询历史
                    print(self.logistics_bot.show_history())
                    continue
                
                # 处理输入并返回结果
                response = self.handle_user_input(user_input)
                print(f"\n🤖 助手: {response}")
            except KeyboardInterrupt:
                print("\n🤖 强制退出，再见！")
                break
            except Exception as e:
                error_msg = self.ai_router.get_ai_response(f"程序出错：{str(e)}，请友好告知用户")
                print(f"\n🤖 助手: {error_msg}")

if __name__ == "__main__":
    # 启动机器人（需先配置快递鸟和智谱API凭证）
    bot = SmartRealLogisticsBot()
    bot.run()