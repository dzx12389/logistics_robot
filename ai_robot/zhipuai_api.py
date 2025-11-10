# zhipuai_api.py - 智谱AI接口
from zhipuai import ZhipuAI  # 需先安装：pip install zhipuai

class ZhipuAIAPI:
    def __init__(self):
        # 替换为你的真实智谱API Key（从https://open.bigmodel.cn/获取）
        self.api_key = "f53be3f7ce6b4aa6946924a134f68b49.MYahSNgn8ObzjDUj"
        self.client = ZhipuAI(api_key=self.api_key)
        
        # 系统提示词（定义物流助手角色）
        self.system_prompt = """你是专业的物流助手，专注于以下服务：
        1. 解答运费计算、配送时效、包装建议、保价政策、禁运品等问题
        2. 分析物流异常（如运单不存在、配送延迟等）
        3. 用中文口语化回复，适当添加物流相关emoji（📦🚚⏱️等）
        4. 未知问题直接说明"抱歉，这个问题我不太清楚"
        """
    
    def get_ai_response(self, user_input):
        """调用智谱AI获取回复，带系统提示词"""
        try:
            response = self.client.chat.completions.create(
                model="glm-4",  # 智谱AI的模型名称
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_input}
                ],
                temperature=0.6,  # 控制回复随机性
                max_tokens=500    # 最大回复长度
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"智谱AI调用失败：{str(e)}"

# 确保类被正确定义和导出
if __name__ == "__main__":
    # 简单的自测代码
    api = ZhipuAIAPI()
    print("✅ ZhipuAIAPI 类创建成功")
    print(f"类名: {ZhipuAIAPI.__name__}")