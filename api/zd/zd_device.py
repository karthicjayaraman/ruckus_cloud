from flask import Blueprint,g, request
from flask_cors import cross_origin
import json
import datetime
import os
from bson import json_util
from ..lib.data_tables import big_table
from ..lib.data_graphs import data_graph
zd_device = Blueprint('zd_device', __name__, url_prefix='/zd')


@zd_device.route('/get_config_devices')
@cross_origin()
def get_config_devices():
        columns=['mac','nameandip','model','version']
        device_sql="select "+",".join(columns)+" from zd_devices";
        result=[];
        data = g.conn.select_advanced(device_sql);
        for row in data:
                row_data=dict(zip(columns, row));
                row_datanamenip=[];
                row_datanamenipstr=str(row_data['nameandip'])
                row_datanamenip=row_datanamenipstr.split("/")
                row_data['Name']=row_datanamenip[1];
                row_data['IP Address']=row_datanamenip[0];

                result.append(row_data);
        return json.dumps(result, default=json_util.default)




@zd_device.route('/zd_device_info', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def zd_device_info():
        zdip='';
        if request.method == 'POST':
                json_data = request.get_json()
                zdip=json_data.get("zd_ip", "")
        else:
                return json.dumps({}, default=json_util.default)
        con_dev_sql="""select 
z.ZDIP, c.threshold, c.uptime,
c.noclient, c.memory, z.TotalClients, z.TotalAPs,z.RXBytesMB,
z.TXBytesMB,z.TotalBytesMB, z.RXPacketsMP, z.TXPacketsMP, 
z.TotalPacketsMP,
c.serial_console, c.SNMP2, c.SNMP3
from `zd_config_devices` c,
`zd_APGroup_Threshold` z 
where 
c.mac_add = z.MAC and z.ZDIP='"""+zdip+"""'"""
        data = g.conn.select_advanced(con_dev_sql);
        data = data[0]
        print data
        result={}
        thres_row=["zdconnectedaps","zduptime","zdnoofclients","zdusedmemory","apnoofclients","apnoofaps","aprxbytes","apxbytes","apotalbytes","aprxpacket","aptxpackets","aptotalpacket"]
        thres_num=0;
        result["mac"]=data[0]
        for thres in thres_row:
                thres_num=thres_num+1;
                thres_data=data[thres_num].split("/")
                thres_dict={}
                thres_dict["enabled"]=thres_data[0]
                thres_dict["compare"]=thres_data[2]
                thres_dict["limit"]=thres_data[1]
                thres_dict["ssh"]=thres_data[3]
                thres_dict["snmp"]=thres_data[4]
                result[thres]=thres_dict
        zd=data[13].split("###")
        result["zd"]={"enabled":zd[0],"username":zd[1],"password":zd[2]}
	snmp2=data[14].split("###")
        result["snmp2"]={"enabled":snmp2[0],"key":snmp2[1]}
        snmp3=data[15].split("###")
        result["snmp3"]={"enabled":snmp3[0],"username":snmp3[1],"password":snmp3[2],"method":snmp3[3]}
        return json.dumps(result, default=json_util.default)



@zd_device.route('/zd_ping_test', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def zd_ping_test():
        zdip='';
        if request.method == 'POST':
                json_data = request.get_json()
                zdip=json_data.get("zd_ip", "")
        else:
                return json.dumps({"result":"zd not given"}, default=json_util.default)

        response = os.system("ping -c 1 " + zdip)
        if response==0:
                response="reachable"
        else:
                response="not reachable"
        result={"status":response}
        return json.dumps(result, default=json_util.default)


@zd_device.route('/zd_add_device', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def zd_add_device():
        if request.method == 'POST':
                ip=""
                json_data = request.get_json()
                try:
                        ip=json_data.get("zd_ip","")
                except Exception:
                        return json.dumps({"result":"ZD IP not given"}, default=json_util.default)
                if ip=="":
                        return json.dumps({"result":"ZD IP not given"}, default=json_util.default)
                if find_zd(ip)>0:
                        return json.dumps({"result":"ZD IP is already available"}, default=json_util.default)
                else:
                        result=add_zd(json_data);
                        return json.dumps({"result":"ZD IP added successfully","info":result}, default=json_util.default)
        else:
                return json.dumps({"result":"ZD not given"}, default=json_util.default)





def find_zd(ip):
       
        check_sql="select nameandip from zd_devices where nameandip like '%%"+ip+"%%' ";
        data = g.conn.select_advanced(check_sql);
        return len(data);


def add_zd(json_data):
        ip=json_data.get("zd_ip","")
        ssh_value=""
        snmp2_value=""
        snmp3_value=""
        try:
                ssh=json_data.get("zd","")
                print ssh
                ssh_value=ssh["enabled"]+"###"+ssh["username"]+"###"+ssh["password"]
                snmp2=json_data.get("snmp2","")
                snmp2_value=snmp2["enabled"]+"###"+snmp2["key"]
                snmp3=json_data.get("snmp3","")
                snmp3_value=snmp3["enabled"]+"###"+snmp3["username"]+"###"+snmp3["password"]+"###"+snmp3["method"]
        except Exception:
                pass
        thres_data={}
        thres_row=["zdconnectedaps","zduptime","zdnoofclients","zdusedmemory","apnoofclients","apnoofaps","aprxbytes","apxbytes","apotalbytes","aprxpacket","aptxpackets","aptotalpacket"]
        for thres in thres_row:
                value=""
                try:
                       col=json_data.get(thres,"")
                       col_data=[]
                       for key in ["enabled","compare","limit","ssh","snmp"]:
                               col_data.append(col[key])
                       value="/".join(col_data)
                except Exception:
                       pass
                thres_data[thres]=value
        ins_res=[]
        try:
                last_row= g.conn.insert('zd_APGroup_Threshold',ZDIP=ip)
        except Exception:
                result="ZD_device not inserted"
                ins_res.append(result)
        try:
                last_row= g.conn.insert('zd_config_devices',serial_console=ssh_value,SNMP2=snmp2_value,SNMP3=snmp3_value,
                        threshold=thres_data["zdconnectedaps"],uptime=thres_data["zduptime"],noclient=thres_data["zdnoofclients"],memory=thres_data["zdusedmemory"],mac_add='',cpu='',prcess='',space='',byte_trans='',smartredun='',)
        except Exception:
                result="zd_config_devices not inserted"
                ins_res.append(result)
        try:
                last_row= g.conn.insert('zd_APGroup_Threshold', TotalClients=thres_data['apnoofclients'],
                        TotalAPs =thres_data['apnoofaps'],RXBytesMB =thres_data['aprxbytes'],TXBytesMB =thres_data['apxbytes'],TotalBytesMB=thres_data['apotalbytes'],
                        RXPacketsMP=thres_data['aprxpacket'],TXPacketsMP=thres_data['aptxpackets'],TotalPacketsMP=thres_data['aptotalpacket'],
                        MAC='',ZDIP=ip,APGroupName='',CommonGroup='')
        except Exception:
                result="zd_Threshold not inserted"
                ins_res.append(result)
        result={"ip":ip,"inserted_result":ins_res}
        return result



