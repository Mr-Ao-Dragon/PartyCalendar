from datetime import datetime

def convert_time_start(date_str):
    # 解析字符串 "2025.01.10" 为 datetime 对象
    date_obj = datetime.strptime(date_str, "%Y.%m.%d")

    # 转换为 'yyyyMMdd' 格式的字符串
    new_date_str = date_obj.strftime("%Y%m%d")
    return new_date_str

def convert_time_end(date_str):
    # 解析字符串 "2025.01.10" 为 datetime 对象
    date_obj = datetime.strptime(date_str, "%Y.%m.%d")
    
    # 将 datetime 对象转为 Unix 时间戳（秒级别）
    timestamp = int(date_obj.timestamp())
    
    # 增加一天（86400秒）
    # new_timestamp = timestamp + 86400
    
    # 将增加一天后的时间戳转为 datetime 对象
    new_date_obj = datetime.fromtimestamp(timestamp)
    
    # 转换为 'yyyyMMdd' 格式的字符串
    new_date_str = new_date_obj.strftime("%Y%m%d")
    
    return new_date_str


def get_today_date():
    """ 获取当前日期 (年-月-日) """
    return datetime.now().date()