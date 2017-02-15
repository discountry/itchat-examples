#!/usr/bin/env python3
import itchat
from itchat.content import TEXT

@itchat.msg_register(TEXT, isGroupChat=False)
def text_reply(msg):
    print(msg)
    if 'IFE' in msg['Text']:
      friend = itchat.search_friends(userName=msg['FromUserName'])
      print(friend)
      itchat.get_chatrooms(update=True)
      chatroom = itchat.search_chatrooms('2017IFE抱团群')[0]
      print(chatroom)
      r = itchat.add_member_into_chatroom(chatroom['UserName'], [friend])
      if r['BaseResponse']['ErrMsg'] == '':
        itchat.send(('自动邀请成功！'), msg['FromUserName'])

itchat.auto_login(enableCmdQR=True,hotReload=True)
itchat.run()
