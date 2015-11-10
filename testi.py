#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import requests
login={"login":{"user":"sdn","password":"skyline","domain":"sdn"}}
host = "https://130.230.115.203:8443"
kohde= "130.230.115.233"
monitor_dpid="00:02:3c:a8:2a:47:d9:80"
monitor_port ="23"


def get_token(logindata):
    headers = {'Content-Type': 'application/json'}
    req = requests.post(host+'/sdn/v2.0/auth', headers=headers, data=json.dumps(logindata), verify='sdncertti')
    # make an exectpion if not 200 ok
    req.raise_for_status()
    # it loads the json from the string
    authtoken = json.loads(req.text)
    token = authtoken["record"]["token"]
    return token

def get_datapaths(token):
    headers = {'Content-Type': 'application/json', 'X-Auth-Token' : token}
    req =requests.get(host+'/sdn/v2.0/of/datapaths', headers=headers, verify='sdncertti')
    req.raise_for_status()
    dpidt=json.loads(req.text)
    retarr = []
    # get rid of completely useless outer key
    for dpen in dpidt["datapaths"]:
        retarr.append(dpen["dpid"])
    return retarr

# T
def get_nodes(token):
    headers = {'Content-Type': 'application/json', 'X-Auth-Token' : token}
    req = requests.get(host+'/sdn/v2.0/net/nodes', headers=headers, verify='sdncertti')
    req.raise_for_status()
    return req.text

#GET /sdn/v2.0/of/datapaths/{dpid}/flows
def get_flows(dpid,token):
    headers = {'Content-Type': 'application/json', 'X-Auth-Token' : token}
    req = requests.get(host+'/sdn/v2.0/of/datapaths/'+dpid+'/flows', headers=headers, verify='sdncertti')
    req.raise_for_status()
    return req.text

def dpid_from_ip(ip,token):
    end_devices=get_nodes(token)
    devices_list=json.loads(end_devices)
    if 'nodes' not in devices_list:
        raise ValueError("Not a nodes list")
    if 'ip' not in devices_list["nodes"][0]:
        raise ValueError("No valid data for any target")
    for node in devices_list["nodes"]:
        if (node["ip"] == ip ):
            return node["dpid"]
    return ""


token = get_token(login)
# Now use the token inside a X-Auth:
#datapathids = get_datapaths(token)

end_devices=get_nodes(token)
#print end_devices
target_dpi=dpid_from_ip(kohde,token)
flowit=get_flows(target_dpi,token)
print flowit

# dpid

#for dpid in datapathids:
#    print json.dumps(json.loads(get_flows(dpid,token)), indent=4, sort_keys=True)
