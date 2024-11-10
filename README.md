# PartyCalendar

兽聚档期日历

使用 Python3 基于开发

# 使用

使用以下命令用于补全缺失的Python库文件

```sh
pip install -r requirements.txt
```

启动 兽聚档期日历自动更新

```sh
py3 main.py
```

启动后，在项目的根目录下面将会生成：

* app.log

- events.ics


# 订阅日历

打开手机日历，找到订阅日历行程功能

订阅日历

```http
http://xxx.xxx.xxx.xxx/PartyCalendar/events.ics
```

如果你有域名，也可以通过域名访问

```http
http://furcw.fun/PartyCalendar/events.ics
```

在使用时请务必记得将 `PartyCalendar` 文件夹设置成可 `共享访问`

若不进行此设置，可能会导致无法正常访问到 `events.ics` 文件
