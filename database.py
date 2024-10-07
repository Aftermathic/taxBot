from replit import db

def clearDatabase():
    db.clear()

def getVotes():
    if ("votes" in db.keys()):
        return db["votes"]
    else:
        return "None"

def votes(userid, vote):
    if ("votes" in db.keys()):
        voters = db["votes"]
        if (str(userid) in voters):
            return False
        else:
            voters[str(userid)] = vote
            return True
    else:
        db["votes"] = {
            str(userid): vote
        }

def setRunningMate(userid, userid2):
    if ("running_mates" in db.keys()):
        running_mates = db["running_mates"]
        running_mates[userid] = userid2
    else:
        db["running_mates"] = {
            userid: userid2
        }

def getRunningMate(userid):
    if ("running_mates" in db.keys()):
        running_mates = db["running_mates"]
        if (userid in running_mates):
            return running_mates[userid]
        else:
            running_mates[userid] = "None"
            return "None"
    else:
        return False

def getBalance(userid):
    balances = None
    if ("balances" in db.keys()):
        balances = db["balances"]
    else:
        db["balances"] = {
            userid: 1000
        }
        
        balances = db["balances"]

    return balances[userid]

def addToBalance(userid, amount):
    if ("balances" in db.keys()):
        balances = db["balances"]
        
        if (userid in balances):
            current = balances[userid] 
            balances[userid] = current + abs(amount)
        else:
            balances[userid] = 1000 + abs(amount)
        
        db["balances"] = balances
    else:
        db["balances"] = {
            userid: 1000 + abs(amount)
        }

def subtractFromBalance(userid, amount):
    if ("balances" in db.keys()):
        balances = db["balances"]
        
        if (userid in balances):
            current = balances[userid] 
            balances[userid] = current - abs(amount)
        else:
            balances[userid] = 1000 - abs(amount)

        db["balances"] = balances
    else:
        db["balances"] = {
            userid: 1000 - abs(amount)
        }