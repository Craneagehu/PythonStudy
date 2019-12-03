import socket
import struct
import re
from threading import Thread
import time

sk_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# tcp 连接
host = socket.gethostbyname("openbarrage.douyutv.com")
# 斗鱼服务器地址
port = 8601
# 端口号
sk_client.connect((host, port))


# 创建连接

def send_msg(msg):  # 根据弹幕协议，对斗鱼服务器发送信息格式处理。
    content = msg.encode()
    length = len(content) + 8
    code = 689
    head = struct.pack('i', length) + struct.pack('i', length) + struct.pack('i', code)
    try:
        sk_client.sendall(head + content)
    except:
        time.sleep(2)


def init(room_id):  # 登录信息
    msg_login = 'type@=loginreq/roomid@={}/\x00'.format(room_id)
    # 若连接其他直播间在roomid@=（）/内添加直播间号
    send_msg(msg_login)
    time.sleep(1)
    msg_join = 'type@=joingroup/rid@=74751/gid@=-9999/\x00'
    # 同上
    send_msg(msg_join)


def keep_live():  # 心跳包，保持连接斗鱼弹幕服务器
    while True:
        time.sleep(15)
        msg_keep = 'type@=mrkl/\x00'
        send_msg(msg_keep)


def get_dm():  # 获取弹幕

    pattern = re.compile(b'type@=chatmsg/.+?/nn@=(.+?)/txt@=(.+?)/.+?/level@=(.+?)/')
    # re提取数据格式
    while 1:
        buffer = b''
        while 1:
            recv_data = sk_client.recv(4096)  # 获取数据，定义数据大小
            buffer += recv_data  # 将数据传入buffer
            if recv_data.endswith(b'\x00'):
                break
        for nn, txt, level in pattern.findall(buffer):
            try:
                print("[lv.{:0<2}][{}]: {}".format(level.decode(), nn.decode(), txt.decode().strip()))
        # 输出得到内容
            except UnicodeDecodeError as e:
                print(e)


def main(room_id):
    init(room_id)  # 向斗鱼弹幕服务器发送连接请求
    t1 = Thread(target=get_dm)  # 获取弹幕
    t2 = Thread(target=keep_live)  # 保持心跳在线
    t1.start()  # 开启线程
    t2.start()


if __name__ == '__main__':
    room_id = '208114'
    main(room_id)