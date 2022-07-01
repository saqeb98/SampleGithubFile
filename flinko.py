import time
from aifc import Error

import requests
import json

class Test_Failed(Error):
    pass

def login(mail, password):
    s = requests.Session()
    payload = {
        'emailId': mail,
        'password': password,
    }
    logurl = 'https://app.flinko.com:8101/optimize/v1/public/user/signin'
    head = {
        "accept": "application/json",
        "Content-Type": "application/json"
    }
    resp = requests.post(logurl, json=payload)
    tk = json.loads(resp.content)
    token = tk['responseObject']['access_token']
    head["Authorization"] = "Bearer " + token

    suiteid = 'SUITE1003'
    pes = s.post('https://app.flinko.com:8109/optimize/v1/dashboard/execution/suite/' + suiteid, headers=head)
    out = json.loads(pes.content)
    exid = out['responseObject']['id']

    time.sleep(2)
    sc = 0
    while (sc < 1):
        r1 = s.get('https://app.flinko.com:8109/optimize/v1/dashboard/execution/' + exid, headers=head)
        c1 = json.loads(r1.content)
        fr1 = c1['responseObject']['executionStatus']
        print(fr1)
        if (fr1 == "Completed" or fr1 == "Terminated" or fr1 == "Warning"):
            if fr1 == 'Completed':
                r2 = s.get('https://app.flinko.com:8110/optimize/v1/executionResponse/result/' + exid, headers=head)
                c2 = json.loads(r2.content)
                fr2 = c2['responseObject']['suiteStatus']
                print("End Result : " + fr2)
                sc = 1
            elif (fr1 == "Terminated" or fr1 == 'Warning'):
                 print("End Result : " + fr1)
                 sc = 1
        time.sleep(10)

login('sheerazzulfi123@gmail.com', 'Ali5171*')
