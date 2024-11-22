import time
from flask import Flask, render_template
import dataGET, sysLog
import updataICS

app = Flask(__name__,template_folder='pages')
logger = sysLog.setup_logger()

# 重新与数据源服务器建立链接
def retryServer(errorType: int) -> str:
    """
    传入 errorType 数值
    如果最后无法与数据源服务器建立链接
    将返回 errorServer 并结束运行
    """
    while errorType < 6:
        logger.error("")
        logger.error("无法获得兽聚日历信息!")
        logger.error("将在五秒钟后尝试重新获取兽聚日历信息!")
        logger.error(f"已经重试获取次数:{errorType}")
        logger.error("")
        errorType = errorType + 1
        if errorType == 6:
            logger.error("")
            logger.error("与数据所提供服务器建立连接失败!")
            return 'errorServer'
        time.sleep(5)  # 等待5秒

@app.route('/')
def index():  # put application's code here
    return render_template('./index.html')

@app.route('/events')
def events(): # 全部聚会的档期日历
    errorType = 0
    eventsData = dataGET.furParty_GET()

    # 判断是否已正常链接 API 服务器
    if eventsData['code'] != 'OK':
        retryServer(errorType)
    
    print(updataICS.disposeAPI(eventsData))


    return eventsData

if __name__ == '__main__':
    app.run()
