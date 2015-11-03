### This is data graph library for generic function for many graphs
### This will respond the jsons for the graph which are all getting inputs as column names, days and table name
### Date Created: Sep 25th, 2015
### Originated By Hariharaselvam Balasubramanian (4470)

from flask import Blueprint,g
import json
import datetime
import re
from bson import json_util

def data_graph(**params):
	### Get parameters
	days = params['days']
	tablename= params['tablename']
	column_one= params['column_one']
	column_two= params['column_two']
	timestamp_col= params['timestamp_col']
	where_condition= params['where_condition']
	convert = params['convert']
	### Get Max Datetime from DB
	max_datetime=""
	try:
		max_datetime=g.conn.select_advanced(" SELECT MAX( "+timestamp_col+" ) FROM "+tablename);
		max_datetime=max_datetime[0].strftime("%Y-%m-%d %H:%M:%S")
	except Exception:
		max_datetime="";
	### Generate SQL 
	graph_sql = "select "+column_one+" , "+column_two+" , "+timestamp_col+" from "+tablename+" where "+where_condition+" and "+timestamp_col+">=DATE_SUB('"+max_datetime+"',INTERVAL "+str(days)+" DAY) ORDER BY "+timestamp_col+" asc";
	### Get Data from DB
	data =[]
	try:
        	data = g.conn.select_advanced(graph_sql);
	except Exception:
		data = []
        series_list=[];
	### Initiate JSON data
        json_string='[ { "name" : "Show/Hide All" } ';
	### Distinct Serial names
        for row in data:
                if row[0] not in series_list:
                        series_list.append(row[0]);
	### Sort data
	data.sort(key=lambda x: x[2])
	### Generate Serial Data
        for series in series_list:
                graph_data=[]
                for row in data:
                        if row[0]==series:
				### Get and convert Timestamp
				timestamp=""
				try:
                                	timestamp=str(row[2]);
                                	timestamp=int(datetime.datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S").strftime('%s')) * 1000;
				except Exception:
					timestamp="00000000"
				### Get and convert Count
                                count=row[1];
				if convert == 'uptime':
					count= convert_to_min(row[1]);
				if convert == 'percent':
					count= convert_percent(row[1]);
				### Each Timestamp of Series
                                if count != None:
                                        graph_data.append("["+str(timestamp)+","+str(count)+"]");
		### Complete Data of Each Series
                json_string=json_string+', { "name" : "'+series+'" , "data" : '+'[ '+', '.join(graph_data)+' ] }';
	### Complete JSON data
        json_string=json_string+' ]';
        return json_string;
                	
def bytes_graph(**params):
	json_string=""
        days = params['days']
	scgip = params['scgip']
        tablename = params['tablename']
        where_condition= params['where_condition']
	### Get Max Datetime from DB
        max_datetime=""
        try:
                max_datetime=g.conn.select_advanced(" SELECT MAX( Timestamp ) FROM "+tablename);
                max_datetime=max_datetime[0].strftime("%Y-%m-%d %H:%M:%S")
		max_datetime="'"+max_datetime+"'"
        except Exception:
                max_datetime="CURDATE()";
	graph_sql = "SELECT RXMBytes,TXMBytes,TotalMBytes,Timestamp FROM "+tablename+" where SCGIP='"+scgip+"' and "+where_condition+" and Timestamp>=DATE_SUB("+max_datetime+",INTERVAL "+str(days)+" DAY) order by Timestamp asc";
	data = []
	try:
		data = g.conn.select_advanced(data_sql);
	except Exception:
		pass
        rxmbytes_list=[]
        txmbytes_list=[]
        tombytes_list=[]
	for row in data:
		if len(row)==4:
			timestamp=str(row[3]);
			timestamp=int(datetime.datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S").strftime('%s')) * 1000;
			rxmbytes_list.append("["+str(timestamp)+","+str(row[0])+"]");
			txmbytes_list.append("["+str(timestamp)+","+str(row[1])+"]");
			tombytes_list.append("["+str(timestamp)+","+str(row[2])+"]");
	json_string='[ { "name" : "Show/Hide All" } ';
        json_string=json_string+', { "name" : "rxmbytes" ,    "data" : '+'[ '+', '.join(rxmbytes_list)+' ] }';
        json_string=json_string+', { "name" : "txmbytes" ,    "data" : '+'[ '+', '.join(txmbytes_list)+' ] }';
        json_string=json_string+', { "name" : "totalmbytes" , "data" : '+'[ '+', '.join(tombytes_list)+' ] }';
        json_string=json_string+' ]';
	return json_string;


def convert_to_min(uptime):
	pat="\d+[a-z]"
	uptime=re.findall(pat,uptime)
        day=0;
        hour=0;
        min=0;
        sec=0;
        for upt in uptime:
                if upt.endswith('d'):
                        day=int(upt[:-1]);
                        continue;
                        continue;
                if upt.endswith('h'):
                        hour=int(upt[:-1]);
                        continue;
                if upt.endswith('m'):
                        min=int(upt[:-1]);
                        continue;
                if upt.endswith('s'):
                        sec=int(upt[:-1]);
        result=(day*24*60)+(hour*60)+(min*1)+int(sec/60)
        return result;

def convert_percent(percent):
	percent=percent.replace("%","")
	return int(percent)

def convert_timestamp(search_time):
        print search_time
        try:
                dtime=datetime.datetime.strptime(search_time,"%b %d, %Y %H:%M");
                print dtime
                search_time=dtime.strftime("%Y-%m-%d %H:%M")
        except Exception:
                pass
        return str(search_time)
