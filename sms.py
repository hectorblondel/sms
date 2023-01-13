import os
from requests.api import get,post
import json
from time import time
from random import randrange
from datetime import date,datetime
from key import KEY

gateway = "+33648069191"
gateway_formated = "%2B"+gateway[1:]

with open("senders.json",'r') as f:
    senders = json.load(f)


possibles = ["orsay","alba","saclay"]


vus_uuid = []

t = time()
while True :
    tt = time() 
    if tt - t > 5. :
        t = tt
        for s in senders :
            resp = get("https://api.httpsms.com/v1/messages?owner={}&contact={}&limit=1".format(gateway_formated,"%2B"+s[1:]),\
                headers={'accept': 'application/json', 'x-api-Key':KEY})
            if resp.status_code == 200 :
                dico = resp.json()
                #print("dico")
                #print(dico)
                if len(dico["data"]) > 0 :
                    uuid = dico["data"][0]["id"]
                    ticket_type = dico["data"][0]["content"].lower().rstrip()
                    if ticket_type in possibles and (uuid not in vus_uuid) :
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
                        if dico['data'][0]['content'].lower().rstrip() == "alba":
                            pass
                        with open('templates/'+ticket_type+'.txt','r') as f :
                            chn = f.read().format(debut,fin,date,code)
                        
                        headers = {'x-api-key': KEY,'Content-Type': 'application/json'}
                        json_data = {'from': gateway,'to': s,'content': chn[:-1]}
                        print("envoi de message de type "+ ticket_type +" à "+s)
                        response = post('https://api.httpsms.com/v1/messages/send', headers=headers, json=json_data)
