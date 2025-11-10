# 🛠️ 快递查询机器人代码修改指南

本指南将帮助您理解和修改快递查询机器人的代码，以满足您的个性化需求。

## 📋 目录

1. [基本配置修改](#1-基本配置修改)
2. [添加新的快递公司](#2-添加新的快递公司)
3. [修改识别规则](#3-修改识别规则)
4. [调整查询逻辑](#4-调整查询逻辑)
5. [修改输出格式](#5-修改输出格式)
6. [常见问题解决](#6-常见问题解决)

## 1. 基本配置修改

### 1.1 设置快递鸟凭证
打开 `logistics_bot_enhanced.py` 文件，找到 `__init__` 方法：

```python
def __init__(self):
    """
    初始化物流查询机器人
    """
    # TODO: 请替换为您自己的快递鸟凭证
    self.e_business_id = "你的商户ID"  # 替换为您的商户ID
    self.api_key = "你的APIKey"        # 替换为您的APIKey
    # ...其他代码
```

### 1.2 修改超时设置
```python
self.timeout = 10  # 将10改为您想要的超时时间（秒）
```

### 1.3 修改历史记录限制
```python
def show_history(self, limit: int = 10) -> str:  # 将10改为您想要的记录条数限制
```

## 2. 添加新的快递公司

### 2.1 添加到快递公司映射
找到 `self.shipper_map` 字典，添加新的快递公司：

```python
self.shipper_map = {
    # ...现有代码
    'NEW': '新快递公司名称',  # 添加新的快递公司
}
```

### 2.2 添加识别规则
找到 `self.shipper_rules` 列表，添加新的识别规则：

```python
self.shipper_rules = [
    # ...现有代码
    # 添加新的识别规则
    {'code': 'NEW', 'name': '新快递公司名称', 'pattern': r'^NEW\d{12,15}$'},
]
```

**正则表达式说明：**
- `^` 表示字符串开始
- `NEW` 表示单号前缀
- `\d{12,15}` 表示12-15位数字
- `$` 表示字符串结束

### 2.3 添加模糊匹配规则
找到 `auto_recognize_shipper` 方法中的 `prefix_map`：

```python
prefix_map = {
    # ...现有代码
    'NW': 'NEW',  # 添加新的前缀匹配
}
```

## 3. 修改识别规则

### 3.1 调整现有规则
您可以修改现有的正则表达式来调整识别规则：

```python
# 例如，修改顺丰的识别规则
{'code': 'SF', 'name': '顺丰速运', 'pattern': r'^SF\d{12,18}$'},  # 将15改为18以支持更长的单号
```

### 3.2 调整识别优先级
修改 `auto_recognize_shipper` 方法中的识别顺序：

```python
def auto_recognize_shipper(self, logistic_code: str) -> Optional[str]:
    try:
        print("\n🔍 正在尝试识别快递公司...")
        
        # 调整这里的顺序可以改变识别优先级
        shipper_code = self.recognize_by_pattern(logistic_code)  # 1. 模式识别
        if shipper_code:
            return shipper_code
        
        shipper_code = self.recognize_by_api(logistic_code)     # 2. API识别
        if shipper_code:
            return shipper_code
        
        shipper_code = self.recognize_by_prefix(logistic_code)  # 3. 前缀识别
        if shipper_code:
            return shipper_code
        
        return None
```

## 4. 调整查询逻辑

### 4.1 修改查询重试机制
找到 `get_logistics_info` 方法，可以添加重试逻辑：

```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
def get_logistics_info(self, logistic_code: str, shipper_code: Optional[str] = None) -> Dict[str, Any]:
    # ...现有代码
```

### 4.2 添加缓存机制
添加缓存以避免重复查询：

```python
from functools import lru_cache

# 在 __init__ 方法中添加
self.cache = {}

def get_logistics_info(self, logistic_code: str, shipper_code: Optional[str] = None) -> Dict[str, Any]:
    # 检查缓存
    cache_key = f"{logistic_code}_{shipper_code}"
    if cache_key in self.cache:
        print("📦 使用缓存数据")
        return self.cache[cache_key]
    
    # ...查询逻辑
    
    # 保存到缓存
    self.cache[cache_key] = result
    return result
```

## 5. 修改输出格式

### 5.1 调整物流轨迹显示
修改 `format_logistics_response` 方法：

```python
def format_logistics_response(self, result: Dict[str, Any]) -> str:
    # ...现有代码
    
    if traces:
        latest_trace = traces[0]
        response += f"\n最新更新：{latest_trace.get('AcceptTime', '')}"
        response += f"\n当前位置：{latest_trace.get('Location', '')}"
        
        response += "\n\n🚚 物流轨迹："
        # 修改这里可以调整轨迹显示格式
        for i, trace in enumerate(reversed(traces), 1):  # 使用reversed显示最新的在前面
            time_str = trace.get('AcceptTime', '')
            station = trace.get('AcceptStation', '')
            response += f"\n{i:2d}. 🕒 {time_str} | 📍 {station}"
    
    return response
```

### 5.2 修改颜色输出
添加颜色支持（需要安装 `colorama` 库）：

```python
from colorama import init, Fore, Style

# 在 __init__ 方法中初始化
init(autoreset=True)

# 在 format_logistics_response 中使用
response += f"\n{Fore.GREEN}📦 快递信息查询结果{Style.RESET_ALL}"
response += f"\n{Fore.CYAN}当前状态：{self.state_map.get(state, state)}{Style.RESET_ALL}"
```

## 6. 常见问题解决

### 6.1 识别失败问题
如果系统无法识别某个快递公司，可以：
1. 检查单号格式是否正确
2. 添加更精确的正则表达式规则
3. 调整识别优先级

### 6.2 查询速度慢
优化方法：
1. 增加超时时间
2. 添加缓存机制
3. 优化识别逻辑

### 6.3 API调用失败
解决方法：
1. 检查网络连接
2. 验证API凭证是否正确
3. 检查API调用次数是否正确
4. 添加重试机制

## 📞 获取帮助

如果您在修改过程中遇到任何问题，可以：
1. 查看代码中的注释
2. 参考快递鸟API文档
3. 检查错误日志
4. 联系技术支持

## 📝 版本历史

- v1.0: 基础功能，支持手动输入编码
- v2.0: 增强版，支持自动识别快递公司
- v2.1: 添加缓存和重试机制
- v2.2: 优化识别算法，提高准确率
