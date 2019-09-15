#!/usr/bin/python3
# coding: utf-8

import poplib
from email.header import decode_header
from email.parser import Parser
from email.utils import parseaddr

def print_msg(msg, indent=0):
    if indent == 0:
        for header in ["From", "To", "Subject", "Date"]:
            value = msg[header]
            if value:
                value = decode_str(value)
            print("%s%s: %s" % (" " * indent, header, value))
    if msg.is_multipart():
        parts = msg.get_payload()
        for n, part in enumerate(parts):
            print("%spart %s" % (" " * indent, n))
            print_msg(part, indent + 1)
    else:
        content_type = msg.get_content_type()
        if content_type == "text/plain" or content_type == "text/html":
            content = msg.get_payload(decode=True)
            charset = get_charset(msg)
            if charset:
                content = content.decode(charset)
            print("%sText: %s" % (" " * indent, content))
        else:
            print("%sAttachment: %s" % (" " * indent, content_type))


def decode_str(s):
    l = decode_header(s)
    value, charset = l[0]
    if charset:
        value = value.decode(charset)

    if len(l) == 2:
        value_tmp = l[1][0]
        value = value + value_tmp.decode(charset)
    return value


def get_charset(msg):
    charset = msg.get_charset()
    if charset is None:
        content_type = msg.get("Content-type", "").lower()
        pos = content_type.find("charset=")
        if pos >= 0:
            charset = content_type[pos + 8:].strip()
    return charset


# 一些参数，从文件读取更加灵活
from_email = "2159628184@qq.com"
from_email_pwd = "wphotxuxctznebjc"
pop_server = "pop.qq.com"
# 连接服务器
server = poplib.POP3(pop_server)
server.set_debuglevel(1)
print(server.getwelcome().decode("utf-8"))
# 登录
server.user(from_email)
server.pass_(from_email_pwd)
# 查看邮箱内的邮件情况
print("Messages: %s Size: %s" % (server.stat())) # 请求服务器发回关于邮箱的统计资料，如邮件总数和总字节数
print(server.list())    # 返回邮件数量和每个邮件的大小
# 获得某一封邮件的内容
resp, mails, octets = server.list() # 返回邮件数量和每个邮件的大小
index = len(mails)  # 获得最后一封的索引
resp, lines, octets = server.retr(index)    # 返回由参数标识的邮件的全部文本
# 解读处理
msg_content = b"\r\n".join(lines).decode("utf-8") # byte字符串
msg = Parser().parsestr(msg_content)    # 解析为普通字符串
print_msg(msg)
# 退出
server.quit()  # 别忘记退出