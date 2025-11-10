# utils.py - 工具函数模块
import re

def extract_tracking_number(text):
    """从用户输入中提取快递单号 - 增强版本"""
    # 移除空格和特殊字符
    clean_text = re.sub(r'\s+', '', text)
    
    # 匹配常见的快递单号格式
    patterns = [
        r'[A-Za-z]{2}\d{8,15}',      # 如 SF123456789
        r'\d{10,15}',                # 纯数字运单号
        r'[A-Za-z]+\d+[A-Za-z]*',    # 混合格式
        r'JD\d{10}',                 # 京东格式
        r'YT\d{10}',                 # 圆通格式
    ]
    
    for pattern in patterns:
        match = re.search(pattern, clean_text)
        if match:
            return match.group().upper()
    return None

def classify_intent(user_input):
    """增强意图分类 - 修复版"""
    user_input_lower = user_input.lower()
    
    # 问候类
    if any(word in user_input_lower for word in ["你好", "您好", "嗨", "hello", "hi"]):
        return "问候"
    # 感谢类
    elif any(word in user_input_lower for word in ["谢谢", "感谢", "thx"]):
        return "感谢"
    # 告别类
    elif any(word in user_input_lower for word in ["再见", "拜拜", "退出", "bye"]):
        return "再见"
    # 功能类
    elif any(word in user_input_lower for word in ["你能做什么", "功能", "帮助", "help"]):
        return "功能"
    # 物流查询类
    elif any(word in user_input_lower for word in ["物流", "快递", "查询", "单号", "track", "包裹", "运单"]):
        return "物流查询"
    # 智能问答类 - 修复：更全面的关键词匹配
    elif any(word in user_input_lower for word in ["运费", "价格", "多少钱", "怎么算", "收费"]):
        return "问运费"
    elif any(word in user_input_lower for word in ["多久", "时效", "几天", "时间", "什么时候到"]):
        return "问时效"
    elif any(word in user_input_lower for word in ["包装", "打包", "包装要求", "怎么包"]):
        return "问包装"
    elif any(word in user_input_lower for word in ["保价", "保险", "赔偿"]):
        return "问保价"
    elif any(word in user_input_lower for word in ["禁运", "不能寄", "限制"]):
        return "问禁运品"
    else:
        return "其他问题"

def format_tracking_response(tracking_info, tracking_number):
    """格式化物流查询结果"""
    if not tracking_info:
        return f"❌ 未找到运单号 {tracking_number} 的物流信息，请检查单号是否正确。"
    
    response = f"📦 运单 {tracking_number} 查询结果：\n"
    response += f"• 快递公司：{tracking_info.get('carrier', '未知')}\n"
    response += f"• 当前状态：{tracking_info['status']}\n"
    response += f"• 当前位置：{tracking_info['location']}\n"
    response += f"• 预计时间：{tracking_info['estimate']}\n"
    response += f"• 最后更新：{tracking_info.get('update_time', '未知')}\n"
    
    # 添加物流轨迹
    if 'history' in tracking_info:
        response += "\n📋 物流轨迹：\n"
        for record in tracking_info['history']:
            response += f"  {record['time']} - {record['event']}\n"
            
    return response