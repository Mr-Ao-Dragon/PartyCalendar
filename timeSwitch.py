from datetime import datetime, time
import pytz


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
    new_timestamp = timestamp + 86400
    
    # 将增加一天后的时间戳转为 datetime 对象
    new_date_obj = datetime.fromtimestamp(new_timestamp)
    
    # 转换为 'yyyyMMdd' 格式的字符串
    new_date_str = new_date_obj.strftime("%Y%m%d")
    
    return new_date_str


def is_after_four_am():
    """
    判断当前时间是否已经到达或超过 4:00 AM。
    返回 True 如果当前时间 >= 4:00 AM，否则返回 False。
    """
    # 获取中国时区
    china_timezone = pytz.timezone('Asia/Shanghai')
    
    # 获取当前时间
    now = datetime.now(china_timezone)
    
    # 获取当天的4:00 AM时间，并转换为 Unix 时间戳
    today = now.date()  # 当前日期
    four_am_time = datetime.combine(today, time(4, 0), tzinfo=china_timezone)  # 4:00 AM
    four_am_timestamp = int(four_am_time.timestamp())  # 4:00 AM的Unix时间戳
    
    # 获取当前时间的 Unix 时间戳（只保留小时和分钟）
    current_time = now.replace(second=0, microsecond=0)  # 当前时间，秒和微秒为0
    current_timestamp = int(current_time.timestamp())  # 当前时间的Unix时间戳
    
    # 判断当前时间是否已到 4:00 AM
    return current_timestamp >= four_am_timestamp


def get_today_date():
    """ 获取当前日期 (年-月-日) """
    return datetime.now().date()