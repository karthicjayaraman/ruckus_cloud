### This is SCG Devices blue print
### This will respond the jsons regarding scg devices such as global config, add, edit, display
### Date: Sep 3rd, 2015

from flask import Blueprint,g, request
from flask_cors import cross_origin
import json
import os
from bson import json_util
scg_device = Blueprint('scg_device', __name__, url_prefix='/scg')



@scg_device.route('/get_config_devices', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def get_config_devices():
        columns=['SCGIP','Model','SerialNumber','SCGVersion','ControlPlaneSoftwareVersion']
        device_sql="select "+",".join(columns)+" from SCG_Devices";
        result=[];
	try:
        	data = g.conn.select_advanced(device_sql);
        	for row in data:
                	result.append(dict(zip(columns, row)))
	except Exception:
		pass
        return json.dumps(result, default=json_util.default)

@scg_device.route('/get_device_info', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def get_device_info():
        scgip='';
        if request.method == 'POST':
                json_data = request.get_json()
                scgip=json_data.get("scg_ip", "")
	else:
		return json.dumps({"result":"SCG IP is not available"}, default=json_util.default)
	con_dev_sql="""select 
		c.SCGIP, c.scg_Ap, c.scg_Noclient,
		s1.ZoneAP, s1.ZoneWlan, s1.ZoneClient, s1.ZoneTxtByte, s1.ZoneRxtByte,
		s2.CpAp, s2.CpUptime, s2.CpClients, s2.CpMemory, 
		s3.DpUptime, s3.DpTunnel,
		c.serial_console, c.SNMP2, c.SNMP3
		from 
		`SCG_Config_Devices` c,
		`SCG_Threshold` s1, 
		`SCG_Threshold` s2, 
		`SCG_Threshold` s3
		where 
		c.SCGIP=s1.SCGIP and s1.Control='Zone' and
		c.SCGIP=s2.SCGIP and s2.Control='ControlPlane' and
		c.SCGIP=s3.SCGIP and s3.Control='DataPlane' and
		c.SCGIP='"""+scgip+"""'"""
	data=[]
	try:
		data = g.conn.select_advanced(con_dev_sql);
		data = data[0]
	except Exception:
		return json.dumps({"result":"SCG IP is not available"}, default=json_util.default)
	
	result={}
	thres_row=["connectedap","apclients","zoneap","zonewlan","zoneclient","zonetxbytes","zonerxbytes","cpap","cpuptime","cpclients",
		"cpmemory","dpuptime","dptunnel"]
	thres_num=0;
	result["ip"]=data[0]
	for thres in thres_row:
		thres_num=thres_num+1;
		thres_data=data[thres_num].split("/")
		thres_dict={}
		if len(thres_data)!=6:
			continue
		thres_dict["enabled"]=thres_data[0]
		thres_dict["compare"]=thres_data[2]
		thres_dict["limit"]=thres_data[1]
		thres_dict["ssh"]=thres_data[3]
		thres_dict["snmp"]=thres_data[4]
		thres_dict["json"]=thres_data[5]
		result[thres]=thres_dict
	try:
		scg=data[14].split("###")
		result["scg"]={"enabled":scg[0],"username":scg[1],"password":scg[2],"enable":scg[3]}
	except Exception:
		result["scg"]={}
	try:
		snmp2=data[15].split("###")
		result["snmp2"]={"enabled":snmp2[0],"key":snmp2[1]}
	except Exception:
		result["snmp2"]={}
	try:
		snmp3=data[16].split("###")
		result["snmp3"]={"enabled":snmp3[0],"username":snmp3[1],"password":snmp3[2],"method":snmp3[3]}	
	except Exception:
		result["snmp3"]={}
	return json.dumps(result, default=json_util.default)
	
@scg_device.route('/scg_ping_test', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def scg_ping_test():
        scgip='';
        if request.method == 'POST':
                json_data = request.get_json()
                scgip=json_data.get("scg_ip", "")
        else:
                return json.dumps({"result":"scg not given"}, default=json_util.default)
	
	response = os.system("ping -c 1 " + scgip)
	if response==0:
		response="reachable"
	else:
		response="not reachable"
	result={"status":response}
	return json.dumps(result, default=json_util.default)

@scg_device.route('/add_device', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def add_device():
	if request.method == 'POST':
		ip=""
		json_data = request.get_json()
		try:
			ip=json_data.get("ip","")
		except Exception:
			return json.dumps({"result":"SCG IP not given"}, default=json_util.default)
		if ip=="":
			return json.dumps({"result":"SCG IP not given"}, default=json_util.default)
		if find_scg(ip)>0:
			return json.dumps({"result":"SCG IP is already available"}, default=json_util.default)
		else:
			result=add_scg(json_data);
			return json.dumps({"result":"SCG IP added successfully","info":result}, default=json_util.default)
	else:
		return json.dumps({"result":"scg not given"}, default=json_util.default)

@scg_device.route('/update_device', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def update_device():
        if request.method == 'POST':
                ip=""
                json_data = request.get_json()
                try:
                        ip=json_data.get("ip","")
                except Exception:
                        return json.dumps({"result":"SCG IP not given"}, default=json_util.default)
                if ip=="":
                        return json.dumps({"result":"SCG IP not given"}, default=json_util.default)
                if find_scg(ip)>0:
                        dresult=delete_scg(ip);
			aresult=add_scg(json_data);
			return json.dumps({"result":"SCG IP updated successfully","del_info":dresult,"add_info":aresult}, default=json_util.default)
                else:
                        return json.dumps({"result":"SCG IP is not available"}, default=json_util.default)
        else:
                return json.dumps({"result":"scg not given"}, default=json_util.default)

@scg_device.route('/delete_device', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def delete_device():
        if request.method == 'POST':
                ip=""
                json_data = request.get_json()
                try:
                        ip=json_data.get("ip","")
		except Exception:
			return json.dumps({"result":"scg not given"}, default=json_util.default)
		if ip=="":
			return json.dumps({"result":"scg not given"}, default=json_util.default)
		if find_scg(ip)>0:
			result=delete_scg(ip);
			return json.dumps(result, default=json_util.default)
		else:
			return json.dumps({"result":"SCG IP is not available"}, default=json_util.default)
	else:
		return json.dumps({"result":"scg not given"}, default=json_util.default)

def find_scg(ip):
	check_sql="select * from SCG_Devices where SCGIP='"+ip+"'";
        data=g.conn.select_advanced(check_sql)
	return len(data);

def delete_scg(ip):
	result={}
	result["ip"]=ip
	try:
                conditional_query='SCGIP = %s';
                dresult= g.conn.delete('SCG_Devices',conditional_query, ip )
                cresult= g.conn.delete('SCG_Config_Devices',conditional_query, ip )
                sresult= g.conn.delete('SCG_Threshold',conditional_query, ip )
                result["status"]="deleted";
        except Exception:
		result["status"]="not deleted";
	return result

def add_scg(json_data):
	ip=json_data.get("ip","")
	ssh_value=""
        snmp2_value=""
        snmp3_value=""
        try:
	        ssh=json_data.get("scg","")
                ssh_value=ssh["enabled"]+"###"+ssh["username"]+"###"+ssh["password"]+"###"+ssh["enable"]
                snmp2=json_data.get("snmp2","")
                snmp2_value=snmp2["enabled"]+"###"+snmp2["key"]
                snmp3=json_data.get("snmp3","")
                snmp3_value=snmp3["enabled"]+"###"+snmp3["username"]+"###"+snmp3["password"]+"###"+snmp3["method"]
        except Exception:
                pass
        thres_data={}
        thres_row=["connectedap","apclients","zoneap","zonewlan","zoneclient","zonetxbytes","zonerxbytes","cpap","cpuptime","cpclients","cpmemory","dpuptime","dptunnel"]
        for thres in thres_row:
                value=""
                try:
 	               col=json_data.get(thres,"")
                       col_data=[]
                       for key in ["enabled","compare","limit","ssh","snmp","json"]: 
	                       col_data.append(col[key])
                       value="/".join(col_data)
                except Exception:
                       pass
        	thres_data[thres]=value
	ins_res=[]
	try:
        	last_row= g.conn.insert('SCG_Devices',SCGIP=ip)
	except Exception:
		result="SCG_device not inserted"
		ins_res.append(result)
	try:
        	last_row= g.conn.insert('SCG_Config_Devices', SCGIP=ip,serial_console=ssh_value,SNMP2=snmp2_value,SNMP3=snmp3_value,
			scg_Ap=thres_data["connectedap"],scg_Noclient=thres_data["apclients"])
	except Exception:
		result="SCG_config_devices not inserted"
		ins_res.append(result)
	try:
        	last_row= g.conn.insert('SCG_Threshold', CpAp=thres_data['cpap'],
			CpUpTime=thres_data['cpuptime'],CpClients=thres_data['cpclients'],CpMemory=thres_data['cpmemory'],
			DpUptime='',DpTunnel='',ZoneAP='',ZoneWlan='',ZoneClient='',ZoneTxtByte='',ZoneRxtByte='',
			SCGIP=ip, ThresholdName='All',Status='ON',Control='ControlPlane' )
	except Exception:
		result="Control Plane SCG_Threshold not inserted"
		ins_res.append(result)
	try:
	        last_row= g.conn.insert('SCG_Threshold', CpAp='',CpUpTime='',CpClients='',CpMemory='',
			DpUptime=thres_data['dpuptime'],DpTunnel=thres_data['dptunnel'],
			ZoneAP='',ZoneWlan='',ZoneClient='',ZoneTxtByte='',ZoneRxtByte='',
			SCGIP=ip, ThresholdName='All',Status='ON',Control='DataPlane' )
	except Exception:
		result="Data Plane SCG_Threshold not inserted"
		ins_res.append(result)
	try:
        	last_row= g.conn.insert('SCG_Threshold', CpAp='',CpUpTime='',CpClients='',CpMemory='',DpUptime='',DpTunnel='',
			ZoneAP=thres_data['zoneap'],ZoneWlan=thres_data['zonewlan'],ZoneClient=thres_data['zoneclient'],
			ZoneTxtByte=thres_data['zonetxbytes'],ZoneRxtByte=thres_data['zonerxbytes'],
			SCGIP=ip, ThresholdName='All',Status='ON',Control='Zone' )
	except Exception:
		result="Zone SCG_Threshold not inserted"
		ins_res.append(result)
        result={"ip":ip,"inserted_result":ins_res}
	return result
