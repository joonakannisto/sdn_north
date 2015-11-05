#!/usr/bin/env python
import json
import requests
#add_header(key, val)
logindata='{"login":{"user":"sdn","password":"skyline","domain":"sdn"}}'

req = requests.post('https://130.230.115.203:8443/api/auth', data=json.dumps(logindata), verify='sdncertti')

print req
