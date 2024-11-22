from datetime import datetime, timedelta
import os
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
def events():
    value = updataICS.disposeAPI(dataGET.furParty_GET())
    return f"{value}"


if __name__ == '__main__':
    app.run(host='192.168.101.169', port=5000)