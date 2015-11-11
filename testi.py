#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import requests
login={"login":{"user":"sdn","password":"skyline","domain":"sdn"}}
host = "https://130.230.115.203:8443"
kohde= "130.230.115.233"
monitor_dpid="00:02:3c:a8:2a:47:d9:80"
monitor_port ="23"

def qheader(token):
    return {'Content-Type': 'application/json', 'X-Auth-Token' : token}


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
    req =requests.get(host+'/sdn/v2.0/of/datapaths', headers=qheader(token), verify='sdncertti')
    req.raise_for_status()
    dpidt=json.loads(req.text)
    retarr = []
    # get rid of completely useless outer key
    for dpen in dpidt["datapaths"]:
        retarr.append(dpen["dpid"])
    return retarr

# T
def get_nodes(token):
    req = requests.get(host+'/sdn/v2.0/net/nodes', headers=qheader(token), verify='sdncertti')
    req.raise_for_status()
    return req.text

#GET /sdn/v2.0/of/datapaths/{dpid}/flows
def get_flows(dpid,token):
    req = requests.get(host+'/sdn/v2.0/of/datapaths/'+dpid+'/flows', headers=qheader(token), verify='sdncertti')
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


def find_inport(flowit,ip):
    flowsj = json.loads(flowit)
    for flowentry in flowjs["flows"]:
        if 'match' in flowentry:
            for rule in flowentry["match"]:
                if(rule["ipv4_src"]==ip):
                    for port_rule in flowentry["match"]:
                        if 'port' in port_rule:
                            return port_rule["port"]

def get_forward_path(src_dpid,dst_dpid,token):
    req = requests.get(host+'/sdn/v2.0/net/paths/forward?src_dpid='+src_dpid+'&dst_dpid='+dst_dpid+'', headers=qheader(token), verify='sdncertti')
    req.raise_for_status()
    return req.text

def addjsonflow(flow,dst_dpid,token):
    req = requests.post(host+'/sdn/v2.0/of/datapaths/'+dst_dpid+'/flows', headers=qheader(token), data=flow, verify='sdncertti')
    req.raise_for_status()
    return req

token = get_token(login)
# Now use the token inside a X-Auth:
#datapathids = get_datapaths(token)

end_devices=get_nodes(token)
#print end_devices
target_dpi=dpid_from_ip(kohde,token)
flowit=get_flows(target_dpi,token)
print flowit


#original_outport =

polku=get_forward_path(target_dpi,monitor_dpid,token)
print polku
forward_path=json.loads(polku)
# Aseta flowt, eli korvaa alkuperäinen kohdeportti forward path ekalla ja toisessa
# dpid:ssä aseta sisääntuleva liikenne portissa x
oldflow=[]
flowtemp=json.loads(flowit)
for flowentry in flowtemp["flows"]:
    if 'match' in flowentry:
        for rule in flowentry["match"]:
            if 'ipv4_src' in rule:
                if(rule["ipv4_src"]==kohde):
                    oldflow.append(flowentry)
                    break

template ="""{
"flow": {
    "cookie": "0x2031987",
    "table_id": 0,
    "priority": 30000,
    "idle_timeout": 300,
    "hard_timeout": 300,
    "match": [
            {"ipv4_src": "10.10.2.1"},
            {"eth_type": "ipv4"}
    ],
    "instructions": [{"apply_actions": [{"output": 2}]}]
}
}"""
flowtemp = json.loads(template)
flowtemp["flow"]["match"][0]["ipv4_src"]=kohde
rewsrc="66.66.66.66.66.66"
newinstruction = json.loads('{"apply_actions": [{"set_field": {"eth_src":"'+rewsrc+'"}},{"output":23}]}')

newinstruction["apply_actions"].append({'output', int(forward_path["path"]["links"][0]["src_port"])})
flowtemp["flow"]["instructions"][0]=newinstruction

print json.dumps(flowtemp, sort_keys=True,indent=4)

#print addjsonflow(json.dumps(flowtemp),target_dpi,token)


#for dpid in datapathids:
#    print json.dumps(json.loads(get_flows(dpid,token)), indent=4, sort_keys=True)
