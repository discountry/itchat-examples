#!/usr/bin/env python3
import itchat
from itchat.content import *

'''
本代码最好运行在python3环境下
运行代码之前先通过pip安装itchat以及pillow
pip install itchat pillow
'''

# 开启自动邀请加入群聊功能的微信群组列表，字典key是好友发来消息的触发关键字，value是群聊的名称，你可以配置相互对应任意数量的关键词：群组
group_dict = {'fcc':'FCC知乎学习小组', '北京':'freecodecamp北京', 'bj':'freecodecamp北京', '100days':'100days', 'ife':'2017IFE','IFE':'2017IFE'}

#自动搜索好友列表，邀请好友加群的主要逻辑
def auto_add_member(msg,roomName):
    friend = itchat.search_friends(userName=msg['FromUserName'])
    print(friend)
    itchat.get_chatrooms(update=True)
    chatroom = itchat.search_chatrooms(roomName)[0]
    print(chatroom['UserName'])
    #如果群聊人数不满100人，可以去掉useInvitation=True，这样好友发送关键字后会被直接加入群
    r = itchat.add_member_into_chatroom(chatroom['UserName'], [friend], useInvitation=True)
    print(r)
    if r['BaseResponse']['ErrMsg'] == '请求成功':
      return '自动邀请加入群聊成功！请等待获取加群链接！'
    else:
      return '请求发生错误，请重试！'

#处理微信聊天消息，根据关键字返回相应群组邀请链接
@itchat.msg_register(TEXT)
def auto_invite_reply(msg):
    if group_dict.has_key(msg['Text']):
        return auto_add_member(msg,group_dict[msg['Text']])

'''
def handle_by_if_reply(msg):
    print(msg)
    if 'IFE' in msg['Text'] or 'ife' in msg['Text']:
      return auto_add_member(msg,'2017IFE抱团群')
    if '签到' in msg['Text'] or '100days' in msg['Text']:
      return auto_add_member(msg,'100days')
    if 'fcc' in msg['Text'] or 'FCC' in msg['Text']:
      return auto_add_member(msg,'FCC知乎学习小组')
'''

# 收到好友邀请自动添加好友
@itchat.msg_register(FRIENDS)
def add_friend(msg):
        print(msg)
        itchat.add_friend(msg['RecommendInfo']['UserName'],status=3,verifyContent='自动添加好友成功！') # 该操作会自动将新好友的消息录入，不需要重载通讯录

'''
如果是在Linux环境下，请设置
enableCmdQR=2
其他操作系统平台请设置
enableCmdQR=True
'''

itchat.auto_login(enableCmdQR=2,hotReload=True)
itchat.run()
