from ics import Calendar, Event

import sysLog
import timeSwitch

logger = sysLog.setup_logger()
events = []

def readAPI(data):
    """
    获得API种所需要的数据
    """

    # 遍历 'data' 列表
    for year_data in data.get('data', []):
        year = year_data.get('year')  # 获取年份
        # print(f"Year: {year}")
        
        # 获取该年的 "data" 列表（每个月的数据）
        for month_data in year_data.get('data', []):
            month = month_data.get('month')  # 获取月份
            # print(f"  Month: {month}")
            
            # 获取该月的所有聚会
            events = month_data.get('list', [])
            
            # 遍历每个聚会的详细信息
            for event in events:
                title = event.get('title')
                name = event.get('name')
                state = event.get('state')
                groups = event.get('groups', [])
                address = event.get('address')
                time_day = event.get('time_day')
                time_start = event.get('time_start')
                time_end = event.get('time_end')

                # 打印每个聚会的详细信息
                # print(f"    Title: {title}")
                # print(f"    Name: {name}")
                # print(f"    State: {state}")
                # print(f"    Groups: {', '.join(groups)}")
                # print(f"    Address: {address}")
                # print(f"    Special: {special}")
                # print(f"    Time Start: {time_start}")
                # print(f"    Time End: {time_end}")
                # print("=" * 40)  # 分隔线
                configICS(title,name,address,time_start,time_end,time_day,state,groups)


def writeICS(events_data):
    """
    写入ICS
    """
   # 创建一个日历对象
    calendar = Calendar()

    # 遍历事件数据并添加事件
    for event_data in events_data:
        event = Event()
        event.name = event_data['SUMMARY']
        event.begin = event_data['DTSTART']+"T020000Z"
        event.end = event_data['DTEND']+"T020000Z"
        event.location = event_data['LOCATION']
        event.description = event_data['DESCRIPTION']
            
        # 将事件添加到日历
        calendar.events.add(event)

    # 保存到 ICS 文件
    with open("events.ics", "w", encoding="utf-8") as file:
        file.writelines(calendar)
    
    




def configICS(title,name,address,time_start,time_end,time_day,state,groups):
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
    if state == 0:
        stateValue = '活动结束'
    if state == 1:
        stateValue = '预告中'
    if state == 2:
        stateValue = '售票中'
    if state == 3:
        stateValue = '活动中'
    if state == 4:
        stateValue = '活动取消'

    formatted_groups = []
    for idx, group in enumerate(groups, start=1):
        formatted_groups.append(f"{idx}:`{group}`")

    groupsValue = ", ".join(formatted_groups)
    timeValue = timeSwitch.get_today_date()
    description = f"档期主题:{name} 活动天数:{time_day} 兽聚状态:{stateValue} 官方QQ群:{groupsValue} 最后更新时间:{timeValue}"
    # 使用空格替换换行符
    description_with_newlines = description.replace(" ", "\n")


    data = {
    "SUMMARY":title,
    "DTSTART":time_start_Value,
    "DTEND":time_end_Value,
    "LOCATION":f"展会所在地:{address}",
    "DESCRIPTION":description_with_newlines
    }

    
    events.append(data)
    writeICS(events)