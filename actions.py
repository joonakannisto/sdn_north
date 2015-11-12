#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import requests
login={"login":{"user":"sdn","password":"skyline","domain":"sdn"}}
host = "https://130.230.115.203:8443"

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

def ether_from_ip(ip,token):
    end_devices=get_nodes(token)
    devices_list=json.loads(end_devices)
    if 'nodes' not in devices_list:
        raise ValueError("Not a nodes list")
    if 'ip' not in devices_list["nodes"][0]:
        raise ValueError("No valid data for any target")
    for node in devices_list["nodes"]:
        if (node["ip"] == ip ):
            return node["mac"]

def better_inport(ip, token):
    end_devices=get_nodes(token)
    devices_list=json.loads(end_devices)
    if 'nodes' not in devices_list:
        raise ValueError("Not a nodes list")
    if 'ip' not in devices_list["nodes"][0]:
        raise ValueError("No valid data for any target")
    for node in devices_list["nodes"]:
        if (node["ip"] == ip ):
            return node["port"]
    return ""

def find_inport(flowit,ip):
    flowsj = json.loads(flowit)
    for flowentry in flowsj["flows"]:
        if 'match' in flowentry:
            for rule in flowentry["match"]:
                if 'ipv4_src' in rule:
                    if(rule["ipv4_src"]==ip):
                        for inportrule in flowentry["match"]:
                            if 'in_port' in inportrule:
                                return inportrule["in_port"]

def flowsforip(flowit,ip):
    flowtemp=json.loads(flowit)
    oldflow=[]
    for flowentry in flowtemp["flows"]:
        if 'match' in flowentry:
            for rule in flowentry["match"]:
                if 'ipv4_src' in rule:
                    if(rule["ipv4_src"]==ip):
                        oldflow.append(flowentry)
                        break
    return oldflow

def get_forward_path(src_dpid,dst_dpid,token):
    req = requests.get(host+'/sdn/v2.0/net/paths/forward?src_dpid='+src_dpid+'&dst_dpid='+dst_dpid+'', headers=qheader(token), verify='sdncertti')
    #req.raise_for_status()
    if response.status_code != 503:
        raise (req.text)
    return req.text

def addjsonflow(flow,dst_dpid,token):
    req = requests.post(host+'/sdn/v2.0/of/datapaths/'+dst_dpid+'/flows', headers=qheader(token), data=flow, verify='sdncertti')
    req.raise_for_status()
    return req
