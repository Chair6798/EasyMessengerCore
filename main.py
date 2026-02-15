from flask import Flask
import json.encoder as json
import hashlib
import time
import re

e_p = re.compile(r'^[a-zA-Z]+$')

# python -m flask --app main run
app = Flask(__name__)

accounts = []

enc = json.JSONEncoder()

sessions = {}

chats = []

def get_default_account():
    return {"username":"", "password":"", "chats": []}

def check_reg_name(name: str)->bool:
    return bool(e_p.fullmatch(name))

def get_account(id):
    return accounts[id]

def find_account(username):
    for account in accounts:
        if account["username"]==username:
            return accounts.index(account)
    return -1

def create_session(account_id):
    if len(accounts)-1<account_id:
        return "wrong"
    sesid = (str(time.time())+str(account_id))
    sessions[sesid] = account_id
    return sesid


def find_account_by_session(session_id: str) -> int:
    try:
        return sessions.get(session_id, -1)
    except Exception:
        return -1


def create_chat(name, root):
    chat = {"name": name, "root": root, "closed":False, "messages": [], "people":[]}
    chats.append(chat)
    return chat

@app.route("/register/<username>/<password>/")
def reg(username,password):
    if find_account(username)!=-1:
        print(f"Failed to create new account. Username {username} is already using")
        return enc.encode({"done":False, "reasoncode":1})
    if check_reg_name(username)==False:
        return enc.encode({"done":False, "reasoncode":2})
    acc = get_default_account().copy()
    acc["username"] = username
    acc["password"] = password
    accounts.append(acc)
    print("Created new account successfully. Username: "+username)
    return enc.encode({"done":True, "reasoncode":0, "session":create_session(len(accounts)-1)})

@app.route("/login/<username>/<password>/")
def login(username,password):
    account_id = find_account(username)
    if account_id==-1:
        print("Failed to login to "+username+" Password wrong!")
        return enc.encode({"done":False, "reasoncode":1})
    account = get_account(account_id)
    if account["password"]==password:
        print("Logged in to "+username+" successfully!")
        return enc.encode({"done":True, "reasoncode":0, "session":create_session(account_id)})
    else:
        print("Failed to login to "+username+" Password wrong!")
        return enc.encode({"done":False, "reasoncode":2})

@app.route("/chats/send/<session>/<chatid>/<message>/")
def sendmessages(session,chatid,message: str):
    chatid=-1
    try:
        chatid=int(chatid)
        if chatid<0 or chatid>len(chats)-1:
            return enc.encode({"done":False,"reasoncode":2})
    except Exception as e:
        return enc.encode({"done":False,"reasoncode":1})
    chat=chats[chatid]
    if not (find_account_by_session(session) in chat["people"]):
        return enc.encode({"done":False,"reasoncode":3})
    if "'" in message or '"' in message:
        return enc.encode({"done":False,"reasoncode":4})
    chat.messages.append({"text":str(message),"userid":find_account_by_session(session)})
    print("sended message")
    return enc.encode({"done":False,"reasoncode":0})

@app.route("/chats/get/<session>/<chatid>/")
def getchat(session,chatid):
    chatid=-1
    try:
        chatid=int(chatid)
        if chatid<0 or chatid>len(chats)-1:
            return enc.encode({"done":False,"reasoncode":2})
    except Exception as e:
        return enc.encode({"done":False,"reasoncode":1})
    chat=chats[chatid]
    if not (find_account_by_session(session) in chat["people"]):
        return enc.encode({"done":False,"reasoncode":3})
    return enc.encode({"done":True,"reasoncode":0,"value":chat})

@app.route("/chats/getchats/<session>/")
def getchats(session):
    userid = find_account_by_session(session)
    if userid == -1:
        return enc.encode({"done":False,"reasoncode":1})
    chatslist = []
    for v in chats:
        if userid in v["people"]:
            chatslist.append({"chat":v,"id":chats.index(v)})
    return enc.encode({"done":True,"reasoncode":0,"value":chatslist})