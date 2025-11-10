# smart_ai_router.py - 智能AI路由
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from local_ai import LocalAI

# 直接在这里定义ZhipuAIAPI类，避免导入问题
try:
    from zhipuai import ZhipuAI
    
    class ZhipuAIAPI:
        def __init__(self):
            self.api_key = "你的智谱API密钥"
            self.client = ZhipuAI(api_key=self.api_key)
            
            self.system_prompt = """你是专业的物流助手，专注于以下服务：
            1. 解答运费计算、配送时效、包装建议、保价政策、禁运品等问题
            2. 分析物流异常（如运单不存在、配送延迟等）
            3. 用中文口语化回复，适当添加物流相关emoji（📦🚚⏱️等）
            4. 未知问题直接说明"抱歉，这个问题我不太清楚"
            """
        
        def get_ai_response(self, user_input):
            try:
                response = self.client.chat.completions.create(
                    model="glm-4",
                    messages=[
                        {"role": "system", "content": self.system_prompt},
                        {"role": "user", "content": user_input}
                    ],
                    temperature=0.6,
                    max_tokens=500
                )
                return response.choices[0].message.content
            except Exception as e:
                return f"智谱AI调用失败：{str(e)}"
                
except ImportError:
    print("❌ zhipuai包未安装，请运行: pip install zhipuai")
    
    class ZhipuAIAPI:
        def __init__(self):
            print("⚠️ 使用备选的ZhipuAIAPI类（zhipuai未安装）")
        
        def get_ai_response(self, user_input):
            return f"智谱AI服务暂不可用（zhipuai包未安装），请安装后重试。原始问题：{user_input}"

class SmartAIRouter:
    def __init__(self):
        self.local_ai = LocalAI()
        self.zhipu_ai = ZhipuAIAPI()
    
    def get_ai_response(self, user_input):
        try:
            response = self.zhipu_ai.get_ai_response(user_input)
            return response
        except Exception as e:
            print(f"⚠️ 智谱AI调用失败，用本地回复：{str(e)}")
            return self.local_ai.get_response(user_input)

# 测试代码
if __name__ == "__main__":
    router = SmartAIRouter()
    print("✅ SmartAIRouter 类创建成功")
    print(router.get_ai_response("你好"))