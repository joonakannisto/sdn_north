#!/usr/bin/env python
import json
import urllib2
#add_header(key, val)
logindata='{"login":{"user":"sdn","password":"skyline","domain":"sdn"}}'

req = urllib2.Request('https://sdn.mi.sec.rd.tut.fi:8443/api/auth')
req.add_header('Content-Type', 'application/json')
response = urllib2.urlopen(req, json.dumps(logindata))

print response
