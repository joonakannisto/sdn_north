#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import actions
import hmac

kohde= "130.230.115.233"
monitor_dpid="00:02:3c:a8:2a:47:d9:80"
monitor_port ="23"

template ="""{"flow": {
"cookie": "0x1751985",
"table_id": 100,
"priority": 30000,
"idle_timeout": 300,
"hard_timeout": 300,
"match": [],
"instructions": []}}"""
token = get_token(login)

target_dpid=dpid_from_ip(kohde,token)

# we don't want to raise any errors here
if (target_dpid !=monitor_dpid):
    polku=get_forward_path(target_dpid,monitor_dpid,token)
else:
    polku = '{"path": {"links" : []}}'
forward_path=json.loads(polku)
# Aseta flowt, eli korvaa alkuperäinen kohdeportti forward path ekalla ja toisessa
# dpid:ssä aseta sisääntuleva liikenne portissa x


uusmac="66:66:66:66:66:66"

templateflow=json.loads(template)
def hairpin(ip,target_sw,target_port_in,target_port_out,rewsrc,token):
    startdpid=dpid_from_ip(ip,token)

    forward_path = {'path':{'links' : []}}
    if (startdpid !=target_sw):
        forward_path=json.loads(get_forward_path(target_dpid,monitor_dpid,token))

    flowit=get_flows(startdpid,token)
    oldflow=flowsforip(flowit,ip)
    origsrc=ether_from_ip(ip,token)
    firstaction = [{'set_field' : {'eth_src' : rewsrc}},{'output' : target_port_in}]
    # we are in the target switch
    #if forwardpath["path"]["links"]
    #    firstaction[0]["output"]=target_port_in
    templateflow.append('apply_actions':firstaction)
    firstelement=True
    previous=1

    for link in forwardpath["path"]["links"]:
        loopflow = templateflow
        if not firstelement:
            loopflow["flow"]["match"].append{'eth_src': rewsrc}
            loopflow["flow"]["match"].append{'port': previous}
            loopaction={'output' : int(link["src_port"])}
            loopflow["flow"]["instructions"]["0"]'apply_actions':loopaction)
        else :
            inport = find_inport(flowit,ip)
            match = [{'ipv4_src' : ip }, {'inport' : inport}]
            loopflow["flow"]["match"]=match
            firstaction[1]={'output': int(link["src_port"])}
            loopflow["flow"]["instructions"]["0"]'apply_actions':firstaction)
            firstelement=False
        addjsonflow(json.dumps(loopflow),link["src_dpid"],token)
        #lets save the destination port in the next switch
        previous=int(link["dst_port"])

    # we are now in the target dpi
    needleflow = templateflow

    needleflow["flow"]["match"].append{'eth_src': rewsrc}
    needleflow["flow"]["match"].append{'port': previous}
    needleaction=[]
    if not forwardpath["path"]["links"]:
        needleaction.append({'set_field' : {'eth_src' : rewsrc}})
    needleaction.append({'output' : target_port_in})
    needleflow["flow"]["instructions"]["0"]'apply_actions':needleaction)
    addjsonflow(json.dumps(needleflow),target_sw,token)
    needleflow["flow"]["match"][1]["port"]=target_port_out
    needleaction=[{'output' : target_port_in}]
    # we could use reversed(forwardpath), but dunno, maybe is asymmetric
    forward_path = {'path':{'links' : []}}
    if (startdpid !=target_sw):
        forward_path=json.loads(get_forward_path(target_dpid,monitor_dpid,token))

        match[0]["inport"]=int(link["dst_port"])
        loopflow["instructions"][0]["apply_actions"]
    newaction[1]["output"] =int(forward_path["path"]["links"][0]["src_port"])
    templateflow["flow"]["instructions"][0].append('apply_actions':[])
    newaction[2]["output"] = newflow["instructions"][0]["apply_actions"][0]

    # does not seem to support more than one action
newflow["instructions"][0]["apply_actions"]=newaction

flowtemp = json.loads(template)
flowtemp["flow"]["match"][0]["ipv4_src"]=kohde

newinstruction = json.loads('{"apply_actions": [{"set_field": {"eth_src":"'+rewsrc+'"}},{"output":23},{"output":42}]}')


flowtemp["flow"]["instructions"][0]=newinstruction

print json.dumps(flowtemp, sort_keys=True,indent=4)

#print addjsonflow(json.dumps(flowtemp),target_dpi,token)


#for dpid in datapathids:
#    print json.dumps(json.loads(get_flows(dpid,token)), indent=4, sort_keys=True)
