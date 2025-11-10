# verify.py - 验证所有组件
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def check_import(module_name, class_name=None):
    try:
        if class_name:
            exec(f"from {module_name} import {class_name}")
            print(f"✅ {module_name}.{class_name} 导入成功")
            return True
        else:
            exec(f"import {module_name}")
            print(f"✅ {module_name} 导入成功")
            return True
    except ImportError as e:
        print(f"❌ {module_name} 导入失败: {e}")
        return False

print("检查所有必要组件...")

# 检查所有必要的导入
modules = [
    ("data", None),
    ("local_ai", "LocalAI"),
    ("utils", "extract_tracking_number"),
    ("utils", "format_tracking_response"),
    ("smart_ai_router", "SmartAIRouter"),
    ("smart_ai_router", "ZhipuAIAPI"),
    ("robot", "LogisticsRobot")
]

all_imports_ok = True
for module, item in modules:
    if not check_import(module, item):
        all_imports_ok = False

if all_imports_ok:
    print("\n🎉 所有组件导入成功！")
    print("尝试启动机器人...")
    try:
        from robot import LogisticsRobot
        robot = LogisticsRobot()
        print("✅ 机器人实例化成功！")
    except Exception as e:
        print(f"❌ 机器人实例化失败: {e}")
else:
    print("\n⚠️ 部分组件导入失败，请检查相关文件")