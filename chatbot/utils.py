# utils.py - 工具函数模块
import random
import time

def extract_tracking_number(text):
    """从用户输入中提取快递单号"""
    words = text.split()
    for word in words:
        # 检查是否包含字母和数字的组合
        if len(word) >= 8 and any(c.isalpha() for c in word) and any(c.isdigit() for c in word):
            return word.upper()
        # 检查纯数字的长单号
        elif len(word) >= 10 and word.isdigit():
            return word
    return None

def classify_intent(user_input):
    """简单意图分类"""
    user_input_lower = user_input.lower()
    
    if any(word in user_input_lower for word in ["你好", "您好", "嗨"]):
        return "问候"
    elif any(word in user_input_lower for word in ["谢谢", "感谢"]):
        return "感谢"
    elif any(word in user_input_lower for word in ["再见", "拜拜", "退出"]):
        return "再见"
    elif any(word in user_input_lower for word in ["你能做什么", "功能", "帮助"]):
        return "功能"
    elif any(word in user_input_lower for word in ["物流", "快递", "查询", "单号"]):
        return "物流查询"
    else:
        return "其他问题"