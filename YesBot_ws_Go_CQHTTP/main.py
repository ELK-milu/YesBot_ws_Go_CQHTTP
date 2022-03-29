# from receive import rev_msg
from send_message.send_message import send_message
from massage_flide import msg_talker
import websocket, time, json, logging
import os,schedule

talker = msg_talker()
print("start")

ws_url = "ws://127.0.0.1:6700/ws"

# 日志设置
logging.basicConfig(level=logging.DEBUG, format='[void] %(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def clear():  # 直接清除房间信息
    path = "G:\\bot\\YesBot_ws_Go_CQHTTP\\room\\"  # 文件夹目录
    files = os.listdir(path)  # 得到文件夹下的所有文件名称
    for file in files:  # 遍历文件夹
        position = path + str(file)  # 构造绝对路径
        with open(position, "a+", encoding='UTF-8') as f:  # 读取遍历的文件
            f.truncate(0)  # 清除文件内容
            f.close()


def time_clear():  # 每个文件每隔6小时修改时间清除房间信息
    localpath = "G:\\bot\\YesBot_ws_Go_CQHTTP\\room\\"  # 文件夹目录
    files = os.listdir(localpath)  # 得到文件夹下的所有文件名称
    for file in files:  # 遍历文件夹
        position = localpath + str(file)  # 构造绝对路径
        with open(position, "a+", encoding='UTF-8') as f:  # 读取遍历的文件
            dtime = os.path.getmtime(position)  # 获取最后修改时间，返回值是标准时间，需要转换
            if time.time() - 21600.0 >= dtime:  # 若系统时间在修改时间6小时后执行
                f.truncate(0)  # 清除文件内容
                f.close()



def recv_msg(_, message):
    try:
        time_clear()
        schedule.every().day.at("02:00").do(clear)  # 每天在凌晨2点运行 clear 函数
        rev = json.loads(message)
        # print(rev)
        if rev == None:
            # print('None.....')
            return False
        else:
            if rev["post_type"] == "message":
                # print(rev) #需要功能自己DIY
                if rev["message_type"] == "private":  #私聊
                    talker.private_msg(rev, ws)
                elif rev["message_type"] == "group":  #群聊

                    talker.group_msg(rev, ws)
                else:
                    pass
            elif rev["post_type"] == "notice":
                if rev["notice_type"] == "group_upload":  # 有人上传群文件
                    pass
                elif rev["notice_type"] == "group_decrease":  # 群成员减少
                    pass
                elif rev["notice_type"] == "group_increase":  # 群成员增加
                    pass
                else:
                    pass
            elif rev["post_type"] == "request":
                if rev["request_type"] == "friend":  # 添加好友请求
                    talker.addFriends(rev, ws)
                    # pass
                if rev["request_type"] == "group":  # 加群请求
                    pass
            else:  # rev["post_type"]=="meta_event":
                pass
    except Exception as e:
        print(e)
        return False
        # continue
    # print(rev["post_type"])


if __name__ == '__main__':

    ws = websocket.WebSocketApp(
        ws_url,
        on_message=recv_msg,
        on_open=lambda _: logger.debug('连接成功......'),
        on_close=lambda _: logger.debug('重连中......'),
    )
    while True:
        ws.run_forever()
        time.sleep(5)