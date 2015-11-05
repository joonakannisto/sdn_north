#!/usr/bin/env python
import json
import requests
#add_header(key, val)
logindata={"login":{"user":"sdn","password":"skyline","domain":"sdn"}}
headers = {'Content-Type': 'application/json'}
req = requests.post('https://sdn.mi.sec.rd.tut.fi:8443/sdn/v2.0/auth', headers=headers, data=json.dumps(logindata), verify=False)
#'sdncertti')

print req
