#!/usr/bin/env python3
import itchat
from itchat.content import *

CHAT_ROOM = '2017IFE抱团群'
TOKEN = 'IFE'

@itchat.msg_register(TEXT, isGroupChat=False)
def text_reply(msg):
    print(msg)
    if TOKEN in msg['Text']:
      friend = itchat.search_friends(userName=msg['FromUserName'])
      print(friend)
      itchat.get_chatrooms(update=True)
      chatroom = itchat.search_chatrooms(CHAT_ROOM)[0]
      print(chatroom)
      r = itchat.add_member_into_chatroom(chatroom['UserName'], [friend])
      if r['BaseResponse']['ErrMsg'] == '':
        itchat.send(('自动邀请成功！'), msg['FromUserName'])

# 收到好友邀请自动添加好友
@itchat.msg_register(FRIENDS)
def add_friend(msg):
    print(msg)
    itchat.add_friend(msg['RecommendInfo']['UserName']) # 该操作会自动将新好友的消息录入，不需要重载通讯录
    itchat.send('自动通过好友请求!', msg['RecommendInfo']['UserName'])

itchat.auto_login(enableCmdQR=True,hotReload=True)
itchat.run()
