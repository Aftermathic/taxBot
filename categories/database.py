from datetime import datetime, timedelta
from replit import db

# use to format numbers {number:,}

def enterVote(userid, party):
    if "votes" in db.keys():
        allVotes = db["votes"]

        
def createDueDates(userid, tax=True, loan=False):
    next_week = datetime.today() + timedelta(days=7)
    next_week_day = next_week.day
    next_week_month = next_week.month
    next_week_year = next_week.year

    if "dueDates" in db.keys():
        dictionary = db["dueDates"]
        taxDate = [next_week_day, next_week_month, next_week_year]
        loanDate = [next_week_day, next_week_month, next_week_year]

        current_data = dictionary.get(str(userid), [taxDate, None])
        current_data[0] = taxDate if tax else current_data[0]
        current_data[1] = loanDate if loan else current_data[1]

        dictionary[str(userid)] = current_data
    else:
        db["dueDates"] = {
            str(userid): [[next_week_day, next_week_month, next_week_year], None]
        }

def getDueDates(userid):
    next_week = datetime.today() + timedelta(days=7)
    next_week_day = next_week.day
    next_week_month = next_week.month
    next_week_year = next_week.year

    if "dueDates" in db.keys():
        dictionary = db["dueDates"]
        dueDates = dictionary.get(str(userid))
        return dueDates
    else:
        db["dueDates"] = {
            str(userid): [[next_week_day, next_week_month, next_week_year], None]
        }

def giveMoney(userid, amount):
    if "balances" in db.keys():
        dictionary = db["balances"]
        currentBalance = dictionary.get(str(userid), 0)
        dictionary[str(userid)] = currentBalance + amount

        db["balances"] = dictionary
    else:
        db["balances"] = {
            str(userid): amount,
            "bank": 100000
        }     

def takeMoney(userid, amount):
    if "balances" in db.keys():
        dictionary = db["balances"]
        currentBalance = dictionary.get(str(userid), 0)
        dictionary[str(userid)] = currentBalance - amount

        db["balances"] = dictionary
    else:
        db["balances"] = {
            str(userid): -amount,
            "bank": 100000
        }

def getBalance(userid):
    if "balances" in db.keys():
        dictionary = db["balances"]

        currentBalance = dictionary.get(str(userid), 0)
        return currentBalance
    else:
        db["balances"] = {
            str(userid): 0,
            "bank": 100000
        }

        return 0

def checkBankBalance():
    if "balances" in db.keys():
        dictionary = db["balances"]

        currentBalance = dictionary.get("bank", 10000)
        return currentBalance
    else:
        db["balances"] = {
            "bank": 100000
        }

        return 100000