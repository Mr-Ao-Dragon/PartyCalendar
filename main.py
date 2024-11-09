from datetime import datetime
import json
import os
import time
import dataGET ,sysLog
import atexit

import timeSwitch
import updataICS

# 定义服务端状态
Star = False
ServerData = ''
has_received_data = False  # 标志位，确保只显示一次 "已收到数据"
has_updated_today = False  # 标志位，确保今天只更新一次数据

# 使用日志模块
logger = sysLog.setup_logger()


def cleanup():
   logger.info("服务端已停止!")

def set_error_type(new_error_type):
    global errorType  # 声明使用全局变量
    errorType = new_error_type

def set_Server_type(new_Server_type):
    global ServerData
    ServerData = new_Server_type

set_error_type(0)
set_Server_type('')


logger.info("服务端已经启动啦～")
Star = True

def getParty():
    """
    服务端通过 getParty() 启动获取数据
    """
    # 调用 dataGET.getFurParty() 获得兽聚日历的 JSON
    logger.info("正在获取兽聚日历的信息,请耐心等待ing")
    data = dataGET.getFurParty()
    # data = dataGET.getFurParty()
    if data['code'] == 'OK':
        logger.info("兽聚日历的信息已经获取啦!")
        logger.info("========================================")
        logger.info("")
        logger.info(f"特别感谢: {data['source']} 所提供的数据支持!")
        logger.info("")
        logger.info("========================================")
        return data
    else:
        logger.error("")
        logger.error("无法获得兽聚日历信息!")
        logger.error(f"{data['source']}")
        logger.error("将在五秒钟后尝试重新获取兽聚日历信息!")
        logger.error(f"已经重试获取次数:{errorType}")
        logger.error("")
        set_error_type(errorType + 1) 
        if errorType == 6:
            logger.error("")
            logger.error("与数据所提供服务器建立连接失败!")
            return 'errorServer'
        return ''
    
# while Star:
#     if len(ServerData) == 0:
#         ServerData = getParty()  # 假设 getParty() 是你获取数据的函数
#         if ServerData == 'errorServer':
#             break
#         if not has_received_data:
#             print("已收到数据")
#             updataICS.readAPI(ServerData)  # 假设 updataICS.readAPI() 用于更新数据
#             has_updated_today = True  # 标记为今天已经更新过
#             has_received_data = True
#         time.sleep(5)  # 等待5秒
#     else:
#         # 判断是否是新的一天
#         today = timeSwitch.get_today_date()
#         if today != timeSwitch.get_today_date():  # 这里可以判断今天是否已经更新过数据
#             has_updated_today = False
        
#         # 检查是否到达4:00 AM 且今天还没有更新过
#         if timeSwitch.is_after_four_am() and not has_updated_today:
#             print("已经到达或超过 4:00 AM!")
#             # 更新数据
#             ServerData = getParty()
#             updataICS.readAPI(ServerData)  # 假设 updataICS.readAPI() 用于更新数据
#             has_updated_today = True  # 标记为今天已经更新过
#         else:
#             print("还未到达 4:00 AM 或 今天已经更新过数据.")
        
#         time.sleep(3600)  # 每小时检查一次


try:
     while Star:
        if len(ServerData) == 0:
            ServerData = getParty()  # 假设 getParty() 是你获取数据的函数
            if ServerData == 'errorServer':
                break
            if not has_received_data:
                logger.info("已收到兽聚日历的数据啦～") 
                updataICS.readAPI(ServerData)  # 假设 updataICS.readAPI() 用于更新数据
                has_updated_today = True  # 标记为今天已经更新过 
                has_received_data = True
            time.sleep(5)  # 等待5秒
        else:
            # 判断是否到达4:00 AM 且今天还没有更新过
            if timeSwitch.is_after_four_am() and not has_updated_today:
                logger.info("已经到达或超过 4:00 AM!")
                # 更新数据
                erverData = getParty()
                updataICS.readAPI(ServerData)  # 假设 updataICS.readAPI() 用于更新数据
                has_updated_today = True  # 标记为今天已经更新过
            else:
                logger.info("还未到达 4:00 AM 或今天已经更新过数据.")
        
            time.sleep(3600)  # 每小时检查一次

except KeyboardInterrupt:
    logger.info("\nCtrl+C 关闭了服务端!")
    logger.info("兽聚日历数据将不再实时更新!")
    pass

# 注册退出时调用的清理函数
atexit.register(cleanup)
