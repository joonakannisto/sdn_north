#!/usr/bin/env python
import json
import requests


def get_token(logindata):
    headers = {'Content-Type': 'application/json'}
    req = requests.post('https://130.230.115.203:8443/sdn/v2.0/auth', headers=headers, data=json.dumps(logindata), verify='sdncertti')
    # make an exectpion if not 200 ok
    req.raise_for_status()
    # it loads the json from the string
    authtoken = json.loads(req.text)
    token = authtoken["record"]["token"]
    return token

def get_datapaths(token):
    headers = {'Content-Type': 'application/json', 'X-Auth-Token' : token}
    req =requests.get('https://130.230.115.203:8443/sdn/v2.0/of/datapaths', headers=headers, verify='sdncertti')
    # make an exectpion if not 200 ok
    req.raise_for_status()
    return req.text

login={"login":{"user":"sdn","password":"skyline","domain":"sdn"}}
token = get_token(login)
print token
# Now use the token inside a X-Auth:
datapaths = get_datapaths(token)
print datapaths
