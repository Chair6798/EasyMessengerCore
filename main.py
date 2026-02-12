from flask import Flask
import json.encoder as json
import hashlib
import time
# python -m flask --app main run
app = Flask(__name__)

accounts = []

enc = json.JSONEncoder()

sessions = {}

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
    
@app.route("/register/<username>/<password>/")
def reg(username,password):
    if find_account(username)!=-1:
        print(f"Failed to create new account. Username {username} is already using")
        return enc.encode({"done":False, "reasoncode":1})
    accounts.append({"username":username,"password":password})
    print("Created new account successfully. Username: "+username)
    return enc.encode({"done":True, "reasoncode":0, "session":create_session(len(accounts)-1)})

@app.route("/login/<username>/<password>/")
def login(username,password):
    account_id = find_account(username)
    if account_id==-1:
        print("Failed to login to "+username+" Password wrong!")
    
    