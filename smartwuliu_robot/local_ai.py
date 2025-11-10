# local_ai.py - 本地智能回复系统
import random

class LocalAI:
    def __init__(self):
        self.conversation_context = {}
        
        self.responses = {
            "greeting": [
                "👋 您好！我是智能物流助手，很高兴为您服务！",
                "🤖 你好！我可以帮您查询物流、计算运费、解答物流问题，有什么可以帮您的？",
                "💫 嗨！欢迎使用物流助手，请问需要什么帮助？"
            ],
            "thanks": [
                "😊 不客气！很高兴能帮助您！",
                "🌟 这是我应该做的！有任何其他问题随时问我！",
                "👍 不用谢！祝您物流顺利！"
            ],
            "goodbye": [
                "👋 再见！祝您生活愉快！",
                "🚀 感谢使用物流助手，期待再次为您服务！",
                "💫 再见！有任何物流问题随时来找我！"
            ],
            "capabilities": [
                "📋 我可以帮您：\n• 查询快递状态\n• 计算运费估算\n• 解答物流问题\n• 提供包装建议\n• 查询快递时效",
                "🛠️ 我的功能包括：\n🔍 物流查询\n💰 运费计算\n⏱️ 时效咨询\n📦 包装指导\n❓ 问题解答",
                "💡 我能为您：\n1. 实时查询快递状态\n2. 估算运费价格\n3. 解答物流疑问\n4. 提供专业建议"
            ],
            "logistics_query": [
                "📦 我可以帮您查询快递状态，请提供运单号。",
                "🔍 需要查询物流信息吗？请告诉我您的快递单号。",
                "🚚 物流查询功能已就绪，请输入您的运单号码。"
            ],
            "fare": [
                "💰 **运费参考标准：**\n\n🏙️ 同城快递：\n• 文件类：8-12元\n• 小包裹：10-15元\n• 大件物品：15-25元\n\n🏢 省内快递：\n• 文件类：10-15元\n• 小包裹：12-18元\n• 大件物品：20-30元\n\n🗺️ 省外快递：\n• 文件类：12-20元\n• 小包裹：15-25元\n• 大件物品：25-40元",
                "📊 **运费计算指南：**\n\n⚖️ 首重1kg价格：\n• 同城：8-12元\n• 省内：10-15元\n• 省外：12-20元\n• 偏远地区：15-25元\n\n📦 续重费用：\n• 每增加1kg：2-8元",
                "💸 **快递费用明细：**\n\n📌 标准快递：\n• 同城：8-15元起\n• 省内：10-20元起\n• 省外：12-25元起"
            ],
            "time": [
                "⏱️ **快递时效参考：**\n\n📦 标准快递：\n• 同城：1-2天\n• 省内：2-3天\n• 省外：3-5天\n• 偏远地区：5-7天",
                "🗓️ **配送时间指南：**\n\n🏙️ 同城配送：\n• 当日达：上午寄，下午到\n• 次日达：今天寄，明天到\n\n🏢 省内配送：\n• 1-2个工作日",
                "📅 **预计到达时间：**\n\n✅ 正常情况：\n• 同城：24小时内\n• 省内：1-2天\n• 省外：2-4天"
            ],
            "packaging": [
                "📦 **包装专业建议：**\n\n📄 文件类：\n• 使用防水快递袋\n• 重要文件建议备份\n\n👕 衣物类：\n• 使用压缩袋节省空间\n• 易脏衣物用塑料袋包裹\n\n🍶 易碎品：\n• 纸箱+气泡膜多层防护\n• 标明『易碎品』",
                "🎁 **物品包装指南：**\n\n✅ 通用要求：\n• 外包装坚固无破损\n• 内填充缓冲材料\n• 地址标签清晰牢固",
                "🛡️ **安全包装要点：**\n\n🔒 防护措施：\n• 纸箱边角用胶带加固\n• 内部空隙用填充物填满"
            ],
            "tracking_help": [
                "🔍 **物流查询方式：**\n\n1. **通过我查询**\n   • 直接告诉我运单号\n   • 我会实时查询状态\n\n2. **官方渠道**\n   • 快递公司官网\n   • 官方APP或小程序",
                "📱 **查询物流信息：**\n\n🎯 最快方法：\n• 把运单号发给我\n• 立即为您查询状态"
            ],
            "default": [
                "🤔 我主要专注于物流相关服务，可以帮您：\n\n🔍 **查询服务**\n• 实时快递状态查询\n• 物流轨迹跟踪\n\n💰 **计算服务**\n• 运费估算\n• 时效预估\n\n请告诉我您需要什么帮助？",
                "💭 作为专业的物流助手，我擅长：\n\n🚚 快递查询 - 实时跟踪包裹\n💸 费用估算 - 帮您预算运费\n⏰ 时效咨询 - 预计到达时间\n\n您想了解哪方面的信息呢？",
                "🎯 我是您的物流小助手，专门处理：\n\n• 📦 包裹追踪和状态查询\n• 💰 运费计算和价格对比\n• ⏱️ 配送时效和预计时间\n\n请随时问我，我很乐意为您服务！"
            ]
        }
    
    def get_response(self, user_input):
        """智能回复主函数"""
        user_input_lower = user_input.lower().strip()
        
        # 问候类
        if any(word in user_input_lower for word in ["你好", "您好", "嗨", "hello", "hi", "早上好", "下午好"]):
            return random.choice(self.responses["greeting"])
        
        # 感谢类
        elif any(word in user_input_lower for word in ["谢谢", "感谢", "thx", "多谢"]):
            return random.choice(self.responses["thanks"])
        
        # 告别类
        elif any(word in user_input_lower for word in ["再见", "拜拜", "退出", "bye", "88"]):
            return random.choice(self.responses["goodbye"])
        
        # 功能查询
        elif any(word in user_input_lower for word in ["你能做什么", "功能", "帮助", "help", "会什么"]):
            return random.choice(self.responses["capabilities"])
        
        # 物流查询
        elif any(word in user_input_lower for word in ["物流", "快递", "查询", "单号", "track", "包裹", "运单", "查一下"]):
            return random.choice(self.responses["logistics_query"])
        
        # 运费查询
        elif any(word in user_input_lower for word in ["运费", "价格", "多少钱", "收费", "费用", "怎么收费"]):
            return random.choice(self.responses["fare"])
        
        # 时效查询
        elif any(word in user_input_lower for word in ["时间", "时效", "几天", "多久", "什么时候到", "几天能到"]):
            return random.choice(self.responses["time"])
        
        # 包装建议
        elif any(word in user_input_lower for word in ["包装", "打包", "怎么包", "如何包装"]):
            return random.choice(self.responses["packaging"])
        
        # 查询帮助
        elif any(word in user_input_lower for word in ["怎么查", "如何查询", "查物流", "哪里查"]):
            return random.choice(self.responses["tracking_help"])
        
        # 默认回复
        else:       
            return random.choice(self.responses["default"])

# 测试代码
if __name__ == "__main__":
    ai = LocalAI()
    print("✅ LocalAI 类创建成功")
    print(ai.get_response("你好"))