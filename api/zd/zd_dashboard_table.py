### This is ZD Dashboard tables blue print
### This will respond the jsons regarding scg dashboard such as, devices

from flask import Blueprint,g, request
from flask_cors import cross_origin
import json
import datetime
from bson import json_util
from ..lib.data_tables import big_table
from ..lib.data_graphs import data_graph
zd_dashboard_table = Blueprint('zd_dashboard_table', __name__, url_prefix='/zd')

### End points 


@zd_dashboard_table.route('/get_devices')
@cross_origin()
def get_devices():
        columns=['MacAddress','NameAndField','UpTime','Model','Version','NumberOfAps','TotalAPCount','NumberOfClientDevices','Status','LocalConnectionStatus','PeerIpIpv6Address']
        device_sql="select "+",".join(columns)+" from zd_Zone_Director_Information";
        result=[];
        data = g.conn.select_advanced(device_sql);
        for row in data:
                row_data=dict(zip(columns, row));
                row_datanamenfield=[];
                row_datanamenfieldstr=str(row_data['NameAndField'])
                row_datanamenfield=row_datanamenfieldstr.split("/")
                row_data['Name']=row_datanamenfield[0];
                row_data['IP Address']=row_datanamenfield[1];
               
                if row_data['TotalAPCount'] > 0:
                           
                                row_data['Noofaps'] = str(row_data['NumberOfAps'])+"/"+str(row_data['TotalAPCount']);
                           
                else:
                           
                                row_data['Noofaps'] = str(row_data['NumberOfAps']);
                           

                result.append(row_data);
        return json.dumps(result, default=json_util.default)





@zd_dashboard_table.route('/get_config_devices')
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
