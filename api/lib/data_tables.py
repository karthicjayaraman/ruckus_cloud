### This is data table library for generic function for all tables with search and paginations
### This will respond the jsons fot table for the given page number and number of rows with search query
### Date Created: Sep 24th, 2015
### Originated By Hariharaselvam Balasubramanian (4470)

from flask import Blueprint,g
import json
from bson import json_util


def big_table(**params):
	page = params['page']
	limit= params['limit']
	tablename= params['tablename']
	columns= params['columns']
	where_condition= params['where_condition']
	search= params['search']
	page = page-1;
	start= limit*page;
	where_clause=" where ";
	#print search
	for key in search:
		where_clause=where_clause+key+" like '%%"+search[key]+"%%' and ";
	where_clause=where_clause+where_condition;
	count_sql="select count(*) from "+tablename;
	full_count_sql=count_sql+" where "+where_condition;
        acdata=[];
        acount=0;
        try:
              acdata = g.conn.select_advanced(full_count_sql);
              acount = acdata[0];
        except Exception:
              pass
	filter_count_sql=count_sql+where_clause;
        fcdata=[];
        fcount=0;
        try:
	      fcdata = g.conn.select_advanced(filter_count_sql);
              fcount = fcdata[0];
        except Exception:
              pass
	if fcount < start:
                start=0;
	#print columns;
	data_sql="select "+",".join(columns)+" from "+tablename+where_clause+" limit  "+str(start)+","+str(limit);
	print "\n"+data_sql+"\n"
        result=[];
        data=[];
        try:
              data = g.conn.select_advanced(data_sql);
        except Exception:
              pass
        for row in data:
                #print row;
                result.append(dict(zip(columns, row)));
        json_data={'count':acount, 'items':result, 'filter_count':fcount };
        #print "\n\n"
	#returns the data as json
        return json.dumps(json_data, default=json_util.default)

                	
def test():
	column_names=['ZoneName','Description','ManagementDomain','CreatedOn','CreatedBy','NumberofWLANs','NumberofAPs','NumberofClients','TunnelType']
	table='ZoneDetails';
	sparams={}
	big_table(tablename=table,where_condition= '1=1',limit=10,page=1,columns=column_names,search=sparams);
#test();



