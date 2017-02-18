#!/usr/bin/env python3
import itchat
from itchat.content import *

group_dict = {'fcc':'FCC知乎学习小组', '北京':'freecodecamp北京', 'bj':'freecodecamp北京', '100days':'100days', 'ife':'2017IFE','IFE':'2017IFE'}

def auto_add_member(msg,roomName):
    friend = itchat.search_friends(userName=msg['FromUserName'])
    print(friend)
    itchat.get_chatrooms(update=True)
    chatroom = itchat.search_chatrooms(roomName)[0]
    print(chatroom['UserName'])
    r = itchat.add_member_into_chatroom(chatroom['UserName'], [friend], useInvitation=True)
    print(r)
    if r['BaseResponse']['ErrMsg'] == '请求成功':
      return '自动邀请加入群聊成功！请等待获取加群链接！'
    else:
      return '请求发生错误，请重试！'

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

itchat.auto_login(enableCmdQR=2,hotReload=True)
itchat.run()
