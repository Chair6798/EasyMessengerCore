from flask import Flask
import json
# python -m flask --app main run
app = Flask(__name__)

accounts = []

def get_account(id):
    return accounts[id]

def found_account(username):
    for account in accounts:
        if account["username"]==username:
            return accounts.index(account)

@app.route("/register/<username>/<password>/")
def reg(username,password):
    accounts.append({"name":username,"password":password})
    print(accounts)
    return "succeful"