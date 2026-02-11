from flask import Flask
import json
# python -m flask --app main run
app = Flask(__name__)

accounts = []

def get_account(id):
    return accounts[id]

def find_account(username):
    for account in accounts:
        if account["username"]==username:
            return accounts.index(account)
    return -1

@app.route("/register/<username>/<password>/")
def reg(username,password):
    if find_account(username)!=-1:
        print(f"Failed to create new account. Username {username} is already using")
        return "usernameusing"
    accounts.append({"username":username,"password":password})
    print("Created new account successfully. Username: "+username)
    return "succes"