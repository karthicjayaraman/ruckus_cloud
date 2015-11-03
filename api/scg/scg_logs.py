### This is SCG logs blue print
### This will respond the jsons regarding scg logs such as global config, add, edit, display
### Date: Sep 9th, 2015



from flask import Blueprint,g, request
from flask_cors import cross_origin
import json
import datetime
from bson import json_util
from ..lib.data_tables import big_table
scg_logs = Blueprint('scg_logs', __name__, url_prefix='/scg')


@scg_logs.route('/logs', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def logs():
        page=1;
        limit=10;
        table="SCG_Logs";
        where="1=1";
	columns=['Timestamp','Content']
        sparams={};
        if request.method == 'POST':
                json_data = request.get_json();
                ### Limit parameters
                limit=json_data.get("limit", "")
                page=json_data.get("page","")
                if limit=='':
                        limit=10;
                else:
                        limit=int(limit);
                if page=='':
                        page=1;
                else:
                        page=int(page);
                ### Search parameters
                Timestamp="";
                Content="";
                Timestamp=json_data.get("Timestamp","")
                Content=json_data.get("Content","")
		if TimeStamp!='' and TimeStamp!=None:
                        sparams['Timestamp']=convert_timestamp(timestamp);
                if Content!='' and Content!=None:
                        sparams['Content']=Content;
        return big_table(tablename=table,where_condition=where,limit=limit,page=page,columns=columns,search=sparams);

def convert_timestamp(search_time):
        print search_time
        try:
                dtime=datetime.datetime.strptime(search_time,"%b %d, %Y %H:%M");
                print dtime
                search_time=dtime.strftime("%Y-%m-%d %H:%M")
        except Exception:
                pass
        return str(search_time)

