#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import actions


kohde= "130.230.115.233"
monitor_dpid="00:02:3c:a8:2a:47:d9:80"
monitor_port ="23"


token = get_token(login)


# Aseta flowt, eli korvaa alkuperäinen kohdeportti forward path ekalla ja toisessa
# dpid:ssä aseta sisääntuleva liikenne portissa x


uusmac="66:66:66:66:66:66"

templateflow=json.loads(template)

def hairpin(ip,target_sw,target_port_in,target_port_out,rewsrc,token):
    template ="""{"flow": {
    "cookie": "0x2342058",
    "table_id": 100,
    "priority": 30000,
    "idle_timeout": 300,
    "hard_timeout": 300,
    "match": [],
    "instructions": []}}"""
    startdpid=dpid_from_ip(ip,token)

    forward_path = {'path':{'links' : []}}
    if (startdpid !=target_sw):
        forward_path=json.loads(get_forward_path(target_dpid,monitor_dpid,token))

    flowit=get_flows(startdpid,token)
    # This is searching only with the source address, TODO: toggle which flow is
    # hairpinned
    oldflow=flowsforip(flowit,ip)
    origsrc=ether_from_ip(ip,token)
    firstaction = [{'set_field' : {'eth_src' : rewsrc}},{'output' : target_port_in}]
    # we are in the target switch
    #if forwardpath["path"]["links"]
    #    firstaction[0]["output"]=target_port_in
    templateflow.append({'apply_actions':firstaction})
    firstelement=True
    previous=find_inport(flowit,ip)

    for link in forward_path["path"]["links"]:
        loopflow = templateflow
        if not firstelement:
            loopflow["flow"]["match"].append({'eth_src': rewsrc})
            loopflow["flow"]["match"].append({'inport': previous})
            loopaction={'output' : int(link["src_port"])}
            loopflow["flow"]["instructions"][0]["apply_actions"]=loopaction
        else :
            #could match here with ether, but what if many ip for one l2?
            match = [{'ipv4_src' : ip }, {'inport' : previous}]
            loopflow["flow"]["match"]=match
            firstaction[1]={'output': int(link["src_port"])}
            loopflow["flow"]["instructions"][0]["apply_actions"]=firstaction
            firstelement=False
        addjsonflow(json.dumps(loopflow),link["src_dpid"],token)
        #lets save the destination port in the next switch
        previous=int(link["dst_port"])

    # we are now in the target dpi
    needleflow = templateflow

    needleflow["flow"]["match"].append({'eth_src': rewsrc})
    needleflow["flow"]["match"].append({'port': previous})

    needleaction=[{'output' : target_port_in}]
    needleflow["flow"]["instructions"].append({'apply_actions':needleaction})
    addjsonflow(json.dumps(needleflow),target_sw,token)


    # we could use reversed(forwardpath), but dunno, maybe is asymmetric, lol
    forward_path = {'path':{'links' : []}}
    if (startdpid !=target_sw):
        forward_path=json.loads(get_forward_path(monitor_dpid,target_dpid,token))
    firstelement=True
    # In addition, not so stupid person would have done this for both directions at once
    for link in forward_path["path"]["links"]:
        loopflow = templateflow
        if not firstelement:
            match = [{'eth_src' : rewsrc }, {'inport' : previous}]
        else :
            match = [{'eth_src' : rewsrc }, {'inport' : target_port_out}]
            firstelement=False

        loopflow["flow"]["match"]=match
        loopaction={'output' : int(link["src_port"])}
        loopflow["flow"]["instructions"][0]["apply_actions"]=loopaction
        addjsonflow(json.dumps(loopflow),link["src_dpid"],token)
        # lets save the destination port in the next switch
        previous=int(link["dst_port"])

    match = [{'eth_src' : rewsrc }, {'inport' : previous}]
    lastaction = [{'set_field' : {'eth_src' : origsrc}},{'output' : target_port_in}]
    for flow in oldflow:
        flow["priority"]=30000
        flow["cookie"]="0x2342058"
        try:
            del flow["duration_sec"]
            del flow["duration_nsec"]
            del flow["packet_count"]
            del flow["flow_mod_flags"]
        # don't give a f for errors :D 
        except KeyError
            pass
        loopflow={'flow': flow}
        addjsonflow(json.dumps(loopflow),startdpid,token)

    # does not seem to support more than one action

#print addjsonflow(json.dumps(flowtemp),target_dpi,token)


#for dpid in datapathids:
#    print json.dumps(json.loads(get_flows(dpid,token)), indent=4, sort_keys=True)
