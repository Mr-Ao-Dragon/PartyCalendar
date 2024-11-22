import logging

# 配置日志模块
def  setup_logger(log_file='app.log'):
    # 创建logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)  # 设置日志等级为 INFO，记录所有日志

    # 创建日志文件处理器，写入日志文件
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.INFO)  # 设置文件日志等级为 INFO

    # 创建日志格式
    formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    file_handler.setFormatter(formatter)

    # 创建控制台处理器，输出日志到终端
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)  # 设置终端日志等级为 INFO
    console_handler.setFormatter(formatter)

    # 将处理器添加到logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

# # 使用日志模块
# logger = setup_logger()
# 
# 示例日志记录
# logger.debug("这是一条DEBUG日志")    # 不会显示在终端，但会写入到文件中
# logger.info("这是一条INFO日志")     # 会显示在终端，并写入到文件中
# logger.warning("这是一条WARNING日志") # 会显示在终端，并写入到文件中
# logger.error("这是一条ERROR日志")    # 会显示在终端，并写入到文件中
# logger.critical("这是一条CRITICAL日志") # 会显示在终端，并写入到文件中
