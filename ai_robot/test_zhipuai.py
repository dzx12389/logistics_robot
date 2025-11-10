# test_zhipuai.py - 完全独立的测试文件，不依赖外部导入
from zhipuai import ZhipuAI  # 确保已安装：pip install zhipuai

# 直接在测试文件中定义ZhipuAIAPI类（绕开导入问题）
class ZhipuAIAPI:
    def __init__(self):
        # 替换为你的真实API Key
        self.api_key = "你的快递鸟API密钥"
        self.client = None
        try:
            self.client = ZhipuAI(api_key=self.api_key)
            print("✅ 智谱AI客户端初始化成功")
        except Exception as e:
            print(f"❌ 智谱AI客户端初始化失败: {str(e)}")
    
    def get_ai_response(self, user_input):
        if not self.client:
            return "客户端未初始化，无法获取回复"
        
        try:
            response = self.client.chat.completions.create(
                model="glm-4",
                messages=[{"role": "user", "content": user_input}]
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"回复获取失败: {str(e)}"

# 测试代码
if __name__ == "__main__":
    print("🧪 开始独立测试...")
    ai = ZhipuAIAPI()
    print("\n测试回复：")
    print(ai.get_ai_response("你好，我想查询快递运费"))