#!/usr/bin/env python3
from peewee import *

db = MySQLDatabase('xxxxx', user='xxxxxx', password='xxxxxxxx', charset='utf8mb4')

class BaseModel(Model):
        class Meta:
                database = db
                
class Question(BaseModel):
        title = CharField(unique=True,max_length=100)
        counter = IntegerField(default=1)

class Answer(BaseModel):
        question = ForeignKeyField(Question, related_name='answers')
        link = CharField(max_length=100)
        content = TextField()

@itchat.msg_register(TEXT, isGroupChat=True, isFriendChat=True)
def text_reply(msg):
    print(msg)
    if msg['FromUserName'] != '@f6c895be24d62305a721755cbf2f0fc9':
        if msg['Text'].split()[0] == 'fcc':
            question_count = search_question('-'.join(msg['Text'].split()[1:])).count()
            if question_count > 0:
                send_answers(msg, search_question('-'.join(msg['Text'].split()[1:])))
                return '已查询到相关解答，请等待回复...'
            else:
                return '未查询到结果，请使用FCC题目包含关键词重试！'
        elif msg['Text'].split(' ',1)[0] == 'add':
            response = add_question(msg['Text'].split(' ',3))
            return response
        elif '帮助' in msg['Text']:
            return '发送 fcc <题目名称> 搜索答案 \n 例如：fcc quote machine \n 发送 add <fcc题目名称> <问题解答解析url> 添加题目解析'
        else:
            return

#Add Questions
def add_question(data):
    print(data)
    print(data[1])
    question = search_question(data[1]).count()
    print(question)
    if question == 1 and validators.url(data[2]) and len(data) >= 3:
        ques = Question.get(Question.title.contains(data[1]))
        Answer.create(question=ques, link=data[2], content=data[3] if len(data) > 3 else '')
        return '添加问答成功，感谢你的贡献~'
    return '请按照 add <fcc题目名称> <问题解答解析url> 的格式发送消息！问题解答必须是合法的url，题目名称与fcc官网url中相同 \n 例如：build-a-random-quote-machine'

# Search Questions
def search_question(keyword):
    questions = Question.select().where(Question.title.contains(keyword)).order_by(Question.counter.desc())
    count_hot_question(questions)
    return questions

def count_hot_question(questions):
    for question in questions:
        query = Question.update(counter=Question.counter + 1).where(Question.title == question.title).execute()
    return True

def send_answers(msg, questions):
    answers = Answer.select().where(Answer.question << questions)
    for answer in answers:
        response = '题目：' + answer.question.title + '\n解答：' + answer.link + '\n说明：'+ answer.content + '\n热度：' + str(answer.question.counter)
        itchat.send(response, msg['FromUserName'])
    if answers:
        return True
    else:
        return False

itchat.auto_login(enableCmdQR=2,hotReload=True, statusStorageDir='fccauto.pkl')
itchat.run()
