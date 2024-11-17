from datetime import datetime, timedelta
import os , atexit , time
import dataGET ,sysLog , updataICS
import subprocess
import threading

# 定义服务端状态
Star = False

# 使用日志模块
logger = sysLog.setup_logger()

def start_http_server():
    # 使用 subprocess 启动 HTTP 服务器
    # `python -m http.server 8000` 会启动一个 HTTP 服务器，监听端口 8000
    logger.info("文件共享已开启 开放端口[8000]")
    logger.info("访问 127.0.0.1:8000 查看是否启动成功")
    with open(os.devnull, 'w') as devnull:
        subprocess.run(["python3", "-m", "http.server", "8000"], stdout=devnull, stderr=devnull)

def run_server_in_background():
    # 使用线程在后台启动 HTTP 服务器
    server_thread = threading.Thread(target=start_http_server)
    server_thread.daemon = True  # 使线程在主程序退出时自动退出
    server_thread.start()
    logger.info("已将线程挂载至后台")

def cleanup():
   logger.info("服务端已停止!")
   logger.info("已关闭文件共享!")

def set_error_type(new_error_type):
    global errorType  # 声明使用全局变量
    errorType = new_error_type

set_error_type(0)


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
            time.sleep(5)  # 等待5秒
            return 'errorServer'
        return ''
    
def main():
    ServerData = ' '
    has_received_data = False  # 标志位，确保只显示一次 "已收到数据"
    try:
        while Star:
            if ServerData == ' ':
                ServerData = getParty()  # 获取数据
                if ServerData == 'errorServer':
                    break
                if not has_received_data:
                    logger.info("已收到兽聚日历的数据啦～")
                    logger.info("日历信息已经更新了～")
                    updataICS.readAPI(ServerData)  # 更新数据
                    has_received_data = True  # 标记为已经收到数据
                    return

    except KeyboardInterrupt:
        logger.info("Ctrl+C 关闭了服务端!")
        logger.info("兽聚日历数据将不再实时更新!")
        pass

def wait_until(target_hour, target_minute, target_second):
    """ 等待直到指定的时间点
    并收集是否已经创建该文件了
    """
    while True:
        now = datetime.now()
        target_time = now.replace(hour=target_hour, minute=target_minute, second=target_second, microsecond=0)
        # 如果目标时间已经过去，设置为明天
        if target_time < now:
            target_time += timedelta(days=1)

        delay = (target_time - now).total_seconds()
        logger.info(f"等待 {delay} 秒，直到 {target_time} 执行 main()")
        time.sleep(delay)  # 等待到目标时间
        # 到达目标时间后执行 main()
        main()

# 注册退出时调用的清理函数
atexit.register(cleanup) 

if __name__ == "__main__":
    # 启动WedServer文件共享
    run_server_in_background()
    if os.path.isfile('events.ics') == False:
        # 没有文件，先初始化一份
        main()
    else:
        # 设定目标时间为每天的 16:00:00
        wait_until(4, 0, 0)