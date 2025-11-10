"""
快递查询机器人配置文件
请在此文件中配置您的快递鸟凭证
"""

# 快递鸟API配置
# 请替换为您自己的快递鸟商户ID和APIKey
# 您可以在快递鸟开发者中心获取这些信息
# https://www.kdniao.com/

EBUSINESS_ID = "你的商户ID"
API_KEY = "你的APIKey"

# API接口地址配置
BASE_URL = "https://api.kdniao.com/Ebusiness/EbusinessOrderHandle.aspx"
RECOGNIZE_URL = "https://api.kdniao.com/api/dist"

# 状态码映射配置
STATE_MAP = {
    '0': '无物流信息',
    '1': '已揽收',
    '2': '运输中',
    '3': '已签收',
    '4': '问题件'
}

# 快递公司编码映射配置
# 可以根据需要添加更多快递公司
SHIPPER_MAP = {
    'SF': '顺丰速运',
    'YT': '圆通速递',
    'ZTO': '中通快递',
    'STO': '申通快递',
    'YD': '韵达快递',
    'HTKY': '百世快递',
    'JD': '京东物流',
    'EMS': 'EMS',
    'YZPY': '邮政快递包裹',
    'JTO': '极兔速递',
    'UC': '优速快递',
    'DBL': '德邦快递',
    'FAST': '快捷快递',
    'ZJS': '宅急送',
    'TNT': 'TNT快递',
    'UPS': 'UPS',
    'DHL': 'DHL',
    'FEDEX': '联邦快递'
}

# 查询配置
TIMEOUT = 10  # 请求超时时间（秒）
HISTORY_LIMIT = 10  # 历史记录显示条数限制

# 日志配置
LOG_ENABLED = False
LOG_FILE = "logistics_bot.log"
