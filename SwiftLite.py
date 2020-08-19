from os import system
from time import time, sleep
from datetime import datetime
import json



#Define color codes
BLACK = "\033[0;30m"
RED = "\033[0;31m"
GREEN = "\033[0;32m"
BROWN = "\033[0;33m"
BLUE = "\033[0;34m"
PURPLE = "\033[0;35m"
CYAN = "\033[0;36m"
LIGHT_GRAY = "\033[0;37m"
DARK_GRAY = "\033[1;30m"
LIGHT_RED = "\033[1;31m"
LIGHT_GREEN = "\033[1;32m"
YELLOW = "\033[1;33m"
LIGHT_BLUE = "\033[1;34m"
LIGHT_PURPLE = "\033[1;35m"
LIGHT_CYAN = "\033[1;36m"
WHITE = "\033[1;37m"
BOLD = "\033[1m"
FAINT = "\033[2m"
ITALIC = "\033[3m"
UNDERLINE = "\033[4m"
BLINK = "\033[5m"
NEGATIVE = "\033[7m"
CROSSED = "\033[9m"
END = "\033[0m"


swiftInput = f'{CYAN}[{WHITE}IN{CYAN}] '
swiftOutput = f'{CYAN}[{WHITE}OUT{CYAN}] '


try:
    from requests_futures.sessions import FuturesSession
except:
    print (f'{swiftOutput}You were missing a library! Installing now . . .')
    sleep(1.5)
    try:
        system('pip install requests-futures')
    except:
        system('python -m pip install requests-futures')

    print (f'{swiftOutput}If you got an error please open command prompt and these commands until it works:')
    print (f'{swiftOutput}pip install requests-futures')
    print (f'{swiftOutput}python -m pip install requests-futures')
    print (f'{swiftOutput}python3 -m pip install requests-futures')
    

session = FuturesSession()

version = '1.0'

def ascii():
    system('cls')
    print(f"""
    {CYAN} ┌──swift Lite v{version}───────────────────────────────────────────┐{WHITE}
                                 _     ____   __
              _____ _      __   (_)   / __/  / /_
             / ___/| | /| / /  / /   / /_   / __/
            (__  ) | |/ |/ /  / /   / __/  / /_
           /____/  |__/|__/  /_/   /_/     \__/

    {CYAN}└────────────────────────────────────── by Teun#2406 ──┘
        """)

ascii()


#Open accounts.txt and create lists for unchecked emails and passwords
try:
    file = open('Accounts.txt', 'r+')
except:
    print (f'{swiftOutput}You did not have a file named Accounts.txt')
    print (f'{swiftOutput}Please create it and restart Swift Lite')
    sleep(5)
    exit()
Lines = file.readlines() 
uncheckedEmails = list()
uncheckedPasswords = list()


#Make accounts go into lists of unchecked emails and passwords
for line in Lines:
    EmailThrowaway = line.split(':')[0]
    EmailThrowaway = EmailThrowaway.replace('\n', '')
    uncheckedEmails.append(EmailThrowaway)
    PasswordThrowaway = line.split(':')[1]
    PasswordThrowaway = PasswordThrowaway.replace('\n', '')
    uncheckedPasswords.append(PasswordThrowaway)



#Print how many accounts there were found
print(f'\n{swiftOutput}Located {len(uncheckedEmails)} account(s)')
if len(uncheckedEmails) > 30:
    print (f'{swiftOutput}You are using more than 30 accounts! Advice is to use 30 at max, or else you might get ratelimited!')


#Ask for the only input needed
print ()
wantedName = input(f'{swiftInput}What name to snipe: ')


#Getting drop time
fourtydaysago = int(time()-3456000)
req = session.get('https://api.mojang.com/users/profiles/minecraft/' + wantedName + '?at=' + str(fourtydaysago))
try:
    req = json.loads(req.result().content)
except:
    print (f'{swiftOutput}That name has never been claimed before, could not find the drop time, please chose a different name')
    sleep(2)
    exit()
olduuid = req["id"]

oldOwnerHistory = session.get('https://api.mojang.com/user/profiles/' + olduuid + '/names')
oldOwnerHistory = json.loads(oldOwnerHistory.result().content)
prevNames = len(oldOwnerHistory)

dropTime = (oldOwnerHistory[prevNames-1]["changedToAt"]/1000)+3196800
if dropTime > time()+172800:
    dropTime = (oldOwnerHistory[prevNames-2]["changedToAt"]/1000)+3196800

if dropTime < time():
    print (f'\n{swiftOutput}That name has already dropped! Please chose a different name')
    sleep(2)
    exit()




#Create even more lists and variables?
Tokens = list()
Passwords = list()
UUIDs = list()
validate_reqs = list()
Emails = list()
reqs = list()


#Calculate time which is later used to see how long it took to log in to the accounts
ms1 = time() * 1000

print (f'{swiftOutput}Waiting to log in')
while True:
    if int(time()) >= dropTime - 3600:
            break


#Send login requests
for i in range (len(uncheckedEmails)):
    validate_reqs.append(session.post('https://authserver.mojang.com/authenticate', json={'agent': {'name': 'Minecraft', 'version': 1},'username': uncheckedEmails[i], 'password': uncheckedPasswords[i]}))
    print (f'{swiftOutput}Sent request to log in to Account {str(i + 1)}')


#Print how long it took to send login requests
print ()
print (f'{swiftOutput}Time it took to log in to {len(uncheckedEmails)} accounts: {int(time()* 1000 - ms1)}ms')
sleep(.5)
print ()


#Receive login requests
for i in range(len(uncheckedEmails)):
    req = validate_reqs[i].result()
    if req.status_code == 200:
        print (f'{swiftOutput}Received response {GREEN}"valid" {CYAN}for account {i + 1} | Status code: {req.status_code}')
        req = json.loads(req.content)
        Tokens.append("Bearer " + req["accessToken"])
        for users in req ['availableProfiles']:
            UUIDs.append(str(users['id']))
        Passwords.append(uncheckedPasswords[i])
        Emails.append(uncheckedEmails[i])
    else:
        print (f'{swiftOutput}Received response {RED}"invalid" {CYAN}for account {i + 1} | Status code: {req.status_code}')
print ()


#Empty request list to save memory
validate_reqs = list()


print (f'{swiftOutput}Working accounts: {len(Emails)} / {len(uncheckedEmails)}')
print (f'{swiftOutput}This means you can send {len(Emails) * 20} requests')
Delay = len(Emails) * 0.4


#Assigning timestamps
grabTime = dropTime - 50
startSniping = dropTime - Delay


#Print when wanted name will drop
print (f'{swiftOutput}Wanted name "{wantedName}" will drop @ ' + str(datetime.fromtimestamp(dropTime).strftime('%H:%M:%S')))
print (f'{swiftOutput}Using Delay: {Delay}')


#A simple while True loop to wait until grabbing bearer tokens
while True:
    if int(time()) >= grabTime:
        print()
        break


#Verifying bearer tokens
reqs_verify = list()
for i in range(len(Emails)):
    reqs_verify.append(session.post("https://api.mojang.com/user/security/challenges", headers={'Authorization':Tokens[i]}))
    print (f'{swiftOutput}Sent request to verify Bearer token {str(i + 1)}')

for i in range (len(Emails)):
    req = json.loads(reqs_verify[i].result().content)
    try:
        questions = list()
        ids = list()
        for qquestion in req ['question']:
            questions.append(qquestion)
            
        for idd in req ['id']:
            ids.append(idd)

        print (f'{swiftOutput}Security questions detected at account {i + 1}')
        answers = list()
        for i in range(3):
            print (f'Question {i + 1}: {questions[i]}')
            answers.append(input('Answer: '))
        payload = {
            "id": ids[0],
            "answer" : answers[0]
        },
        {
            "id": ids[1],
            "answer" : answers[1]
        },
        {
            "id": ids[2],
            "answer" : answers[2]
        }
        session.post("https://api.mojang.com/user/security/location", json = payload, headers={'Authorization':Tokens[i]})
    except:
        print (f'{swiftOutput}Account {i + 1} did not have security questions')
        

#Print thingies
print (f'\n{swiftOutput}Successfully verified all Bearer tokens')
print (f'{swiftOutput}Will start sniping @ {datetime.fromtimestamp(startSniping).strftime("%H:%M:%S")}')


#A simple while True loop to wait until grabbing sniping desired name
while True:
    if time() >= startSniping:
        break

print ()
print (f'{swiftOutput}Started sending requests')


#YEEET
for i in range (len(Emails)):
    for ii in range (20):
        reqs.append(session.post(f'http://api.mojang.com/user/profile/{UUIDs[i]}/name', headers={'Authorization':Tokens[i]}, json={"name":wantedName,"password":Passwords[i]}))

print ()

for i in range(len(Emails) * 20):
    req = reqs[i].result()
    if req.status_code == 400:
        print (f'{swiftOutput}Received response {i + 1} from mojang with status {RED}"Not available"{CYAN} | Status code: {req.status_code} [{time() - startSniping}]')
    
    
    
    elif req.status_code == 401:
        print (f'{swiftOutput}Received response {i + 1} from mojang with status {RED}"Not authorised"{CYAN} | Status code: {req.status_code} [{time() - startSniping}]')
    
    
    
    elif req.status_code == 204:
        print (f'{swiftOutput}Received response {i + 1} from mojang with status {GREEN}"Success"{CYAN} | Status code: {req.status_code} [{time() - startSniping}]')
        print()
        print (f'{swiftOutput}Successfully set name to {wantedName} using Swift Lite v{version}')
        print (f'{swiftOutput}You sniped the name with request {i + 1} !')
        print (f'{swiftOutput}This request was most likely sent with account on line {int(i /20 ) + 1} in Accounts.txt')

        try:
            webbhook = open('webhook.txt', 'r+')
            webhook = webbhook.readlines()
            webhook = DiscordWebhooks(webhook[0])
            webhook.set_content(title='New Snipe!', description=f'Succuessfully sniped name `{wantedName}`!', color=0x72FF33)
            webhook.send()
            print(f'{swiftOutput}Sent message in #Snipes!')
        except:
            print(f'{swiftOutput}Did not find a webhook (or invalid), skipping!')
        try:
            files = {'model':'slim', 'file': ('Skin.png', open('Skin.png', 'rb'))}
            response = session.put('https://api.mojang.com/user/profile/' + UUIDs[int(i /20 )] + '/skin', headers=({"Authorization":Tokens[int((i + 1) /20 )]}), files=files)
            response = response.result()
            print (f'{swiftOutput}Attempted to change skin | Status code: {response.status_code}')
        except:
            print (f'{swiftOutput}Couldnt find a skin file, so not uploading skin')
            print (f'{swiftOutput}If you want to always upload a custom skin at snipe, create a file named Skin.png')

        print (f'{swiftOutput}{Emails[int(i /20 )]}:{Passwords[int(i /20 )]}')
        input(f'{swiftOutput}Press enter to see the rest of the results\n')

        
    elif req.status_code == 429:
        print (f'{swiftOutput}Received response {i + 1} from mojang with status {RED}"RATE LIMIT"{CYAN} | Status code: {req.status_code} [{time() - startSniping}]')
    
    elif req.status_code == 504:
        print (f'{swiftOutput}Received response {i + 1} from mojang with status {RED}"GATEWAY TIMEOUT"{CYAN} | Status code: {req.status_code} [{time() - startSniping}]')
    

    else:
        print (f'{swiftOutput}Received response {i + 1} from mojang with status {RED}"Unknown"{CYAN} | Status code: {req.status_code} [{time() - startSniping}]')


input()