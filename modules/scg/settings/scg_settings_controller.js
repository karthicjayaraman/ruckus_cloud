window[appName].controller('scg_settings_controller',function($scope,$state,$http,$rootScope,$window)
{	
	$scope.innerAccordion = {};	
	$scope.innerAccordion.activeSection = 'email';	
	$scope.showaddswatch= false;
	$scope.confirm_message="";
	$scope.confirm_result="no";
	$scope.showsettingconfirm=false;
	$scope.delete_setting="";
	$scope.url="";
	$scope.param={};

	$scope.navigateAccordion = function(sectionName) 
	{		
		$scope.innerAccordion.activeSection = sectionName;		
	}

	$scope.close_confirm = function(result) 
	{		
		$scope.showsettingconfirm=false;
		if(result=="yes")
		{
			switch($scope.url)
			{
				case 'delete_swatch':
					HttpRequest('post','delete_swatch',window.flaskURL+'scg/delete_swatch',$scope.param);
					HttpRequest('get','get_swatch_config',window.flaskURL+'scg/get_swatch_config','');
					break;

				case 'delete_events':
					HttpRequest('post','delete_events',window.flaskURL+'scg/delete_events',$scope.param);
					HttpRequest('get','get_event_config',window.flaskURL+'scg/get_event_config','');
					break;

				case 'delete_log_alert':
					HttpRequest('post','delete_log_alert',window.flaskURL+'scg/delete_log_alert',$scope.param);
					HttpRequest('get','get_log_alert_config',window.flaskURL+'scg/get_log_alert_config','');
					break;

				case 'update_system_alert':
					HttpRequest('post','update_system_alert',window.flaskURL+'scg/update_system_alert',$scope.param);
					HttpRequest('get','get_system_alert',window.flaskURL+'scg/get_system_alert','');
					break;
			}	
		}		
	}

	$scope.show_update_popup = function(id, param1, param2, popup) 
	{	
	
		switch (popup) 
		{
			case 'showswatchpopup':
				$scope.showswatchpopup = true;
				$scope.id = id;	
				$scope.swatch_value = param1;
				break;
			case 'showeventpopup':
				$scope.showeventpopup = true;
				$scope.event_value = param1;
				$scope.even_severity = param2;
				$scope.id = id;
				break;
			case 'showlogpopup':
				$scope.showlogpopup = true;
				$scope.log_regex = param1;
				$scope.log_type = param2;
				$scope.id = id;
				break;	
		}	
	}

	$scope.close_edit_popup = function(id) 
	{		
		switch (id) 
		{
			case 'showeventpopup':
				$scope.showeventpopup = false;
				break;
			case 'showswatchpopup':
				$scope.showswatchpopup = false;
				break;
			case 'showlogpopup':
				$scope.showlogpopup = false;
				break;
		}			
	}

	function HttpRequest(method,action, URL, parameter) 
	{		
		$rootScope.showLoader = true;		
        	var $promise = '';
        	if(method==="post") 
		{
            		$promise = $http.post(URL, parameter);
        	} 
		else 
		{
            		$promise = $http.get(URL, parameter);
        	}
        	$promise.then(function (response) 
		{
            		var result = angular.fromJson(response.data);
           		processTheData(action, result);			
			$rootScope.showLoader = false;			
        	});
    	};

	function processTheData(action, response) 
	{	
		switch (action) 
		{
			case 'get_email_setting':
				$scope.scg_email_setting = response;
				break;

			case 'get_swatch_config':
				$scope.scg_swatch_config = response;
				break;

			case 'get_event_config':
				$scope.scg_event_config = response;
				break;

			case 'get_log_alert_config':
				$scope.scg_log_alert = response;	
				break;

			case 'get_system_alert':
				$scope.scg_system_alert = response;
				break;

			case 'get_ftp_setting':
				$scope.scg_ftp_setting = response;	
				break;

			case 'get_user_mib':
				$scope.scg_user_mib = response;
				break;
		}
	}

	function show_confirm(message)
	{
		$scope.confirm_message=message;
		$scope.showsettingconfirm=true;
	}

	// Swatch Configurations 

	$scope.add_edit_swatch = function()
	{
		if($scope.id=='')
		{
			param = { "regex":$scope.swatch_value};
			HttpRequest('post','add_swatch',window.flaskURL+'scg/add_swatch',param); 
		}
		else
		{
			param = { "regex":$scope.swatch_value, "id":$scope.id };	
			HttpRequest('post','update_swatch',window.flaskURL+'scg/update_swatch',param);  
		}
		$scope.showswatchpopup = false;	
		HttpRequest('get','get_swatch_config',window.flaskURL+'scg/get_swatch_config','');
	}
	
	$scope.delete_swatch = function(id,swatch) 
	{
		show_confirm("Are You sure to Delete Swatch : '"+swatch+"' ? ");
		$scope.param={"id":id};
		$scope.url="delete_swatch";		
	}
	
	// Event Configurations

	$scope.add_edit_event = function() 
	{	
		if($scope.id=='')
		{
			param= { "regex":$scope.event_value, "severity":$scope.even_severity };
			HttpRequest('post','add_events',window.flaskURL+'scg/add_events',param); 
		}
		else
		{
			param= { "regex":$scope.event_value, "severity":$scope.even_severity,"id":$scope.id };
			HttpRequest('post','update_event',window.flaskURL+'scg/update_event',param); 
		}
		$scope.showeventpopup = false;	
		HttpRequest('get','get_event_config',window.flaskURL+'scg/get_event_config','');		
	}

	$scope.delete_event = function(id,event,severity) 
	{
		show_confirm("Are You sure to Delete Event : ' "+event+" ' with Severity : ' "+severity+" ' ? ");
		$scope.param={"id":id};
		$scope.url="delete_events";		
	}

	// Log Alert Configurations

	$scope.add_edit_log = function() 
	{	
		if($scope.id=='')
		{
			param= { "regex":$scope.log_regex, "type":$scope.log_type }
			HttpRequest('post','add_log_alerts',window.flaskURL+'scg/add_log_alerts',param); 
		}
		else
		{
			param= { "regex":$scope.log_regex, "type":$scope.log_type, "id":$scope.id }
			HttpRequest('post','update_log_alert',window.flaskURL+'scg/update_log_alert',param); 
		}
		$scope.showlogpopup = false;	
		HttpRequest('get','get_log_alert_config',window.flaskURL+'scg/get_log_alert_config','');		
	}

	$scope.delete_log_alert = function(id,regex,type) 
	{
		show_confirm("Are You sure to Delete Log Alert : '"+regex+"' in Type : ' "+type+"'? ");
		$scope.param={"id":id};
		$scope.url="delete_log_alert";		
	}
	
	// MIB file Configurations

	
	// System Alert Configurations

	$scope.system_alert = function(id,text,status,newstatus)
	{
		if(status!=newstatus)
		{
			show_confirm("Are You sure to Change'"+text+"' status to ' "+newstatus+"'? ");
			$scope.param={"id":id, "status":newstatus};
			$scope.url="update_system_alert";	
		}
	}
	// Settings page initial api load

	HttpRequest('get','get_email_setting',window.flaskURL+'scg/get_email_setting',''); 

	HttpRequest('get','get_swatch_config',window.flaskURL+'scg/get_swatch_config',''); 

	HttpRequest('get','get_event_config',window.flaskURL+'scg/get_event_config',''); 

	HttpRequest('get','get_log_alert_config',window.flaskURL+'scg/get_log_alert_config',''); 

	HttpRequest('get','get_system_alert',window.flaskURL+'scg/get_system_alert',''); 

	HttpRequest('get','get_ftp_setting',window.flaskURL+'scg/get_ftp_setting',''); 

	HttpRequest('get','get_user_mib',window.flaskURL+'scg/get_user_mib','');

});
