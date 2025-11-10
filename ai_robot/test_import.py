# test_import.py
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from zhipuai_api import ZhipuAIAPI
    print("✅ ZhipuAIAPI 导入成功")
    print("类定义:", ZhipuAIAPI)
    
    # 测试实例化
    api = ZhipuAIAPI()
    print("✅ 实例化成功")
    
except ImportError as e:
    print("❌ ZhipuAIAPI 导入失败:", e)
    # 检查模块内容
    try:
        import zhipuai_api
        print("模块内容:", dir(zhipuai_api))
    except Exception as e2:
        print("模块导入也失败:", e2)
except Exception as e:
    print("❌ 其他错误:", e)