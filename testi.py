#!/usr/bin/env python
import json
import requests
#add_header(key, val)
logindata={"login":{"user":"sdn","password":"skyline","domain":"sdn"}}
headers = {'Content-Type': 'application/json'}
req = requests.post('https://130.230.115.203:8443/sdn/v2.0/auth', headers=headers, data=json.dumps(logindata), verify='sdncertti')
# make an exectpion if not 200 ok
req.raise_for_status()
# it loads json from the string
authtoken = json.loads(req.text)
