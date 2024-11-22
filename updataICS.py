from ics import Calendar, Event

import sysLog
import timeSwitch

logger = sysLog.setup_logger()
events = []


def readAPI(data):
    """
    获得API种所需要的数据
    """
    if not isinstance(data, dict) or 'data' not in data:
        raise ValueError("Invalid input data format")
    
    def process_year(year_data):
        if not isinstance(year_data, dict) or 'year' not in year_data:
            return
        year = year_data['year']
        # print(f"Year: {year}")
        
        for month_data in year_data.get('data', []):
            process_month(month_data)
    
    def process_month(month_data):
        if not isinstance(month_data, dict) or 'month' not in month_data:
            return
        month = month_data['month']
        # print(f"  Month: {month}")
        
        for event in month_data.get('list', []):
            process_event(event)
    
    def process_event(event):
        if not isinstance(event, dict):
            return
        title = event.get('title')
        name = event.get('name')
        state = event.get('state')
        groups = event.get('groups', [])
        address = event.get('address')
        time_day = event.get('time_day')
        time_start = event.get('time_start')
        time_end = event.get('time_end')
        
        # 打印每个聚会的详细信息
        # print_event_details(title, name, state, groups, address, time_start, time_end, time_day)
        configICS(title, name, address, time_start, time_end, time_day, state, groups)
    
    try:
        for year_data in data.get('data', []):
            process_year(year_data)
    except Exception as e:
        print(f"Error processing data: {e}")
@functools.lru_cache(maxsize=None)
def genICS(events_data):
    """
        写入ICS
        """
    # 创建一个日历对象
    calendar = Calendar()
    
    # 遍历事件数据并添加事件
    for event_data in events_data:
        event = Event()
        event.name = event_data['SUMMARY']
        event.begin = event_data['DTSTART'] + "T020000Z"
        event.end = event_data['DTEND'] + "T020000Z"
        event.location = event_data['LOCATION']
        event.description = event_data['DESCRIPTION']
        
        # 将事件添加到日历
        calendar.events.add(event)
        return calendar

def writeICS(events_data):
    
    # 保存到 ICS 文件
    with open("events.ics", "w", encoding="utf-8") as file:
        file.writelines(genICS(events_data))


def configICS(title, name, address, time_start, time_end, time_day, state, groups):
    """
    生成ICS文件\n
    title:展会名称\n
    name:档期主题\n
    address:展会举办地\n
    time_start:开始时间\n
    time_end:结束时间\n
    time_day:举办天数\n
    state:售票状态[兽聚状态码 0.活动结束 1.预告中 2.售票中 3.活动中 4.活动取消]\n
    groups:官方群聊
    """
    
    # logger.info("生成 events.ics 配置文件ing~")
    
    # 时间换算
    time_start_Value = timeSwitch.convert_time_start(time_start)
    time_end_Value = timeSwitch.convert_time_end(time_end)
    
    # 判断售票状态
    match state:
        case 0:
            stateValue = '活动结束'
        case 1:
            stateValue = '预告中'
        case 2:
            stateValue = '售票中'
        case 3:
            stateValue = '活动中'
        case 4:
            stateValue = '活动取消'
    formatted_groups = []
    for idx, group in enumerate(groups, start=1):
        formatted_groups.append(f"{idx}:`{group}`")
    
    groupsValue = ", ".join(formatted_groups)
    timeValue = timeSwitch.get_today_date()
    description = f"档期主题:{name} 活动天数:{time_day} 兽聚状态:{stateValue} 官方QQ群:{groupsValue} 最后更新时间:{timeValue}"
    # 使用空格替换换行符
    description_with_newlines = description.replace(" ", "\n")
    
    events.append({
        "SUMMARY": title,
        "DTSTART": time_start_Value,
        "DTEND": time_end_Value,
        "LOCATION": f"展会所在地:{address}",
        "DESCRIPTION": description_with_newlines
    })
    writeICS(events)
