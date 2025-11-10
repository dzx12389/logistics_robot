# response_handler.py - 回复处理模块
import random
from data_manager import BASIC_RESPONSES, SMART_RESPONSES

class ResponseHandler:
    def __init__(self):
        pass
    
    def get_basic_response(self, category):
        """获取基本对话回复"""
        responses = BASIC_RESPONSES.get(category, BASIC_RESPONSES["默认"])
        return random.choice(responses)
    
    def get_smart_response(self, question):
        """提供智能回复"""
        question_lower = question.lower()
        
        # 检查是否有匹配的智能回复类别
        if any(word in question_lower for word in ["运费", "价格", "多少钱", "收费"]):
            return random.choice(SMART_RESPONSES["运费"])
        elif any(word in question_lower for word in ["多久", "几天", "时间", "时效"]):
            return random.choice(SMART_RESPONSES["时效"])
        elif any(word in question_lower for word in ["包装", "打包", "怎么寄"]):
            return random.choice(SMART_RESPONSES["包装"])
        elif any(word in question_lower for word in ["找不到", "丢失", "没收到"]):
            return random.choice(SMART_RESPONSES["丢失"])
        else:
            smart_responses = [
                f"关于'{question}'，这涉及到物流服务的具体细节，建议您联系客服获取准确信息。",
                f"您问的'{question}'是个很好的问题，我目前无法提供详细解答，但可以帮您查询物流状态。",
                f"对于'{question}'，我的知识有限，但您可以提供快递单号，我来帮您查询具体物流信息。"
            ]
            return random.choice(smart_responses)