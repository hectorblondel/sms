import os
from requests.api import get,post
from json import loads,dumps
from time import time
from random import randrange
from datetime import date,datetime
from key import KEY

gateway = "+33648069191"
gateway_formated = "%2B"+gateway[1:]
vus_uuid = []

t = time()
while True :
    tt = time() 
    if tt - t > 10. :
        t = tt
        dico = get("https://api.httpsms.com/v1/messages?owner={}&contact=%2B33648069191&limit=1".format(gateway_formated),\
            headers={'accept': 'application/json', 'x-api-Key':KEY}).json()
        uuid = dico["data"][0]["id"]
        if dico["data"][0]["content"] == "ALBA" and (uuid not in vus_uuid) :
            vus_uuid.append(uuid)
            #print(dico['data'][0]['content'])
            l = [str(randrange(10)) for _ in range(12)]
            code = l[0]+l[1]+"'"+l[2]+l[3]+"'"+l[4]+l[5]+"'"+l[6]+l[7]+"'"+l[8]+l[9]+"'"+l[10]+l[11]
            rawdate = str(datetime.today())
            debut = rawdate[11:16]
            heures = int(rawdate[11:13])
            if heures == 23 :
                new_heures = '00'
            else :
                if heures < 9 :
                    new_heures = '0'+str(heures+1)
                else :
                    new_heures = str(heures+1)
            fin = new_heures + rawdate[13:16]
            date = rawdate[8:10]+"."+rawdate[5:7]+"."+rawdate[2:4] 
            #print(debut,fin,date)
            if dico['data'][0]['content'] == "ALBA":
                pass
            with open('templates/alba.txt','r') as f :
                chn = f.read().format(debut,fin,date,code)
            
            headers = {'x-api-key': KEY,'Content-Type': 'application/json'}
            json_data = {'from': gateway,'to': '+33648069191','content': chn[:-1]}
            print("envoi de message...")
            response = post('https://api.httpsms.com/v1/messages/send', headers=headers, json=json_data)
