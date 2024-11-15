# PartyCalendar

兽聚档期日历自动更新至手机日历

使用 Python3 基于开发

# 使用

使用以下命令用于补全缺失的Python库文件

```sh
pip install -r requirements.txt
```

启动 兽聚档期日历自动更新

```sh
python main.py
```

启动后，在项目的根目录下面将会生成：

* app.log

- events.ics


# 订阅日历

打开手机日历，找到订阅日历行程功能

订阅日历

```text
http://xxx.xxx.xxx.xxx:8000/events.ics
```
将 `xxx.xxx.xxx.xxx` 替换为您局域网内,正在运行 `main.py` 的设备IP

即可从手机日历中订阅该日历

在运行 `main.py` 的设备上访问 `127.0.0.1:8000` 来验证是否成功开启了文件共享