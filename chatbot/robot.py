# robot.py - 物流机器人类
import time
from data_manager import LOGISTICS_DATA
from utils import extract_tracking_number, classify_intent
from response_handler import ResponseHandler

class LogisticsRobot:
    def __init__(self):
        self.response_handler = ResponseHandler()
    
    def query_logistics(self, tracking_number):
        """查询物流信息"""
        tracking_number = tracking_number.upper()
        
        if tracking_number in LOGISTICS_DATA:
            info = LOGISTICS_DATA[tracking_number]
            return f"快递单号 {tracking_number} 的状态：\n- 当前状态：{info['status']}\n- 当前位置：{info['location']}\n- 预计时间：{info['estimate']}"
        else:
            # 根据单号前缀提供智能回复
            if tracking_number.startswith(('SF', 'sf')):
                return f"顺丰单号 {tracking_number} 的快递正在运输中，预计1-3天内到达。"
            elif tracking_number.startswith(('YT', 'yt')):
                return f"圆通单号 {tracking_number} 的快递已揽收，正在发往目的地。"
            elif tracking_number.startswith(('JD', 'jd')):
                return f"京东单号 {tracking_number} 的快递已出库，即将开始运输。"
            elif tracking_number.startswith(('ST', 'st')):
                return f"申通单号 {tracking_number} 的快递信息正在更新中，请稍后查询。"
            elif tracking_number.startswith(('ZT', 'zt')):
                return f"中通单号 {tracking_number} 的快递已发货，正在等待揽收。"
            else:
                return f"未找到单号 {tracking_number} 的详细物流信息，但快递已在运输途中，预计3-5天到达。"
    
    def chat(self):
        """主聊天循环"""
        print("=" * 50)
        print("物流助手：您好！我是物流智能助手")
        print("可以帮您查询物流信息或回答相关问题")
        print("=" * 50)
        print("输入'退出'可以结束对话")
        
        while True:
            try:
                user_input = input("\n您：").strip()
                
                if user_input in ["退出", "结束", "bye"]:
                    print(f"物流助手：{self.response_handler.get_basic_response('再见')}")
                    break
                
                if not user_input:
                    print("物流助手：您好像没有说话？")
                    continue
                
                # 意图分类和处理
                intent = classify_intent(user_input)
                
                if intent == "问候":
                    print(f"物流助手：{self.response_handler.get_basic_response('问候')}")
                elif intent == "感谢":
                    print(f"物流助手：{self.response_handler.get_basic_response('感谢')}")
                elif intent == "功能":
                    print(f"物流助手：{self.response_handler.get_basic_response('功能')}")
                elif intent == "物流查询":
                    tracking_number = extract_tracking_number(user_input)
                    if tracking_number:
                        print(f"物流助手：{self.query_logistics(tracking_number)}")
                    else:
                        print("物流助手：请告诉我您的快递单号，我来帮您查询。")
                        tracking_input = input("快递单号：").strip()
                        if tracking_input:
                            print(f"物流助手：{self.query_logistics(tracking_input)}")
                        else:
                            print("物流助手：您没有提供快递单号，无法查询。")
                else:
                    print("物流助手：思考中...")
                    time.sleep(1)
                    response = self.response_handler.get_smart_response(user_input)
                    print(f"物流助手：{response}")
                    
            except KeyboardInterrupt:
                print(f"\n物流助手：{self.response_handler.get_basic_response('再见')}")
                break
            except Exception as e:
                print(f"物流助手：抱歉，出现了错误，请重新输入。")