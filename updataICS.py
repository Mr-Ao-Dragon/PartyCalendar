import functools
from ics import Calendar, Event

import timeSwitch

eventsData = []
events = []

def disposeAPI(data):
    """
    处理从 API 中获得的数据\n
    最后由 configICS() 生成需要的数据内容\n
    存储为 json 类型到 events 列表中
    """
    eventsData.clear()
    events.clear()
    def disposeData():
        for year_data in data.get('data', []):
            for month_data in year_data.get('data', []):
                events = month_data.get('list', [])
                for event in events:
                    eventsData.append(event)

    def sortingData():
        """
        整理每个聚会的详细信息\n
        并通过 configICS() 生成配置文件 
        """
        disposeData()
        # 遍历每个聚会的详细信息
        for event in eventsData:
            title = event.get('title')
            name = event.get('name')
            state = event.get('state')
            groups = event.get('groups', [])
            address = event.get('address')
            time_day = event.get('time_day')
            time_start = event.get('time_start')
            time_end = event.get('time_end')
            
            value = configICS(title,name,address,time_start,time_end,time_day,state,groups)
        return value
    
    return sortingData()

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
    return writeICS(events)

def writeICS(events_data):
    """
    写入ICS
    """
   # 创建一个日历对象
    calendarData = Calendar()
    
    # 遍历事件数据并添加事件
    for event_data in events_data:
        event = Event()
        event.name = event_data['SUMMARY']
        event.begin = event_data['DTSTART']+"T020000Z"
        event.end = event_data['DTEND']+"T020000Z"
        event.location = event_data['LOCATION']
        event.description = event_data['DESCRIPTION']
        # 将事件添加到日历
        calendarData.events.add(event)
    return calendarData