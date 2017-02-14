#!/usr/bin/env python3
import itchat
from itchat.content import *
from peewee import *
import datetime

CHAT_ROOM = '100days'

db = MySQLDatabase('xxxxxxx', user='xxxxxxxxxx', password='xxxxxxxxxxx', charset='utf8mb4')

class BaseModel(Model):
        class Meta:
                database = db

class User(BaseModel):
        username = CharField(unique=True,max_length=100)
        openid = CharField(unique=True,max_length=100)
        count = IntegerField(default=1)
        updated_date = DateTimeField(default=datetime.datetime.now)

@itchat.msg_register(TEXT, isFriendChat=True, isGroupChat=True, isMpChat=True)
def simple_reply(msg):
    if not 'helper' in msg['Text']: return
    friend = itchat.search_friends(nickName=msg['ActualNickName'])
    if friend:
        print(friend)
    print(msg)
    response = response_handler(msg)
    print(response)
    return response

@itchat.msg_register(SYSTEM, isGroupChat=True)
def welcome(msg):
    return '欢迎加入100days挑战，艾特我签到开启你的旅程！'


def response_handler(msg):
    response = ''
    if '签到' in msg['Text'] and 'helper' in msg['Text']:
        response = check_in(msg) + '用户: %s' % msg['ActualNickName']
    elif '检查' in msg['Text'] and 'helper' in msg['Text']:
        response = print_unchecked_username(get_unchecked_member())
    elif '清理' in msg['Text'] and 'helper' in msg['Text']:
        response = delete_unchecked_member(get_unchecked_member())
    elif '排行' in msg['Text'] and 'helper' in msg['Text']:
        response = print_top_members()
    else:
        response = '未定义操作！'
    return response

def check_in(userinfo):
    db.connect()
    if User.select().where(User.username == userinfo['ActualNickName']).count() < 1:
        User.create(username=userinfo['ActualNickName'],openid=userinfo['ActualUserName'])
        return '开始你的100天挑战吧！中断1天就会被踢出袄~'
    if User.get(User.username == userinfo['ActualNickName']).updated_date.date().strftime("%Y-%m-%d") < datetime.datetime.now().strftime("%Y-%m-%d"):
        User.update(updated_date = datetime.datetime.now(),count=User.count + 1).where(User.username == userinfo['ActualNickName']).execute()
        return '签到成功！' + '时间: %s' % User.get(User.username == userinfo['ActualNickName']).updated_date
    return '您今日已签到！'

def get_unchecked_user():
    memberList = []
    itchat.get_friends(update=True)
    unchecked_users = User.select().where(User.updated_date < datetime.datetime.now().strftime("%Y-%m-%d"))
    for user in unchecked_users:
        if itchat.search_friends(nickName=user.username):
            memberList.append(itchat.search_friends(nickName=user.username)[0])
    return memberList

def get_unchecked_member():
    itchat.get_chatrooms(update=True)
    chatroom = itchat.search_chatrooms('100days')[0]
    memberList = []
    itchat.get_friends(update=True)
    unchecked_users = User.select().where(User.updated_date < datetime.datetime.now().strftime("%Y-%m-%d"))
    for user in unchecked_users:
        if [m for m in chatroom['MemberList'] if m['NickName'] == user.username]:
            memberList.append([m for m in chatroom['MemberList'] if m['NickName'] == user.username]
[0])
    return memberList

def print_top_members():
    memberList = []
    top_members = User.select().order_by(User.count.desc()).limit(10)
    content = '签到排行：\n'
    for member in top_members:
        content += member.username + ':' + str(member.count) + '\n'
    return content

def print_unchecked_username(memberList):
    if not memberList:
        return '所有成员均已签到！'
    content = '未签到用户：\n'
    for member in memberList:
        content += member['NickName'] + '\n'
    return content
def delete_unchecked_member(memberList):
    if datetime.datetime.now().hour < 23: return '请在23时以后清理未签到成员！'
    itchat.get_chatrooms(update=True)
    chatroom = itchat.search_chatrooms(CHAT_ROOM)[0]
    print(chatroom)
    itchat.update_chatroom(chatroom['UserName'],detailedMember=True)
    itchat.delete_member_from_chatroom(chatroom['UserName'], memberList)
    return '未签到成员清除完毕！'


itchat.auto_login(enableCmdQR=2,hotReload=True)
itchat.run()
