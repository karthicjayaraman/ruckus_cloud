window[appName].controller('scg_trends_controller',function($scope,$state,$http,$rootScope,$window)
{
	
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
			case 'get_ap_device_data':
			 
			$scope.data = response;
			 
		 
			$scope.clientChart2 = 
			{
        			options: 
				{
            				chart: 
					{
						width:920,
						zoomType: 'x',
						spacingRight:1   
            				},
					plotOptions: 
					{
            					series: {}
        				},
        			},
				xAxis: 
				{
            				type: 'datetime',
					title: 
					{
						text: 'Date and Time'
					}
        			},
				yAxis: 
				{
					type: 'logarithmic',
					title: 
					{
						text: 'AP Count'
		 			},
				},
				plotOptions: 
				{
					series: 
					{
               					cursor: 'pointer',
            				},
					legend: 
					{
          	  				enabled: false
        				}
        			},
				series: $scope.data,
        			title: 
				{
            				text: 'Time vs AP Count'
        			},
				credits: 
				{
     	 				enabled: false
    				}
    			};	
			 
			 
			break;
			
			case 'get_client_device_data':
	 
			$scope.data = response;
		 
			$scope.clientChart1 = 
			{
        			options: 
				{
            				chart: 
					{
						width:920,
						zoomType: 'x',
						spacingRight:1   
            				},
					plotOptions: 
					{
            					series: {}
        				},
        			},
				xAxis: 
				{
            				type: 'datetime',
					title: 
					{
						text: 'Date and Time'
					}
        			},
				yAxis: 
				{
					type: 'logarithmic',
					title: 
					{
						text: 'Client Count'
		 			},
				},
				plotOptions: 
				{
					series: 
					{
               					cursor: 'pointer',
            				},
					legend: 
					{
          	  				enabled: false
        				}
        			},
				series: $scope.data,
        			title: 
				{
            				text: 'Time vs Client Count'
        			},
				credits: 
				{
     	 				enabled: false
    				}
    			};	
				
			break;	 
		
		}
	
	 }

	HttpRequest('get','get_client_device_data',window.flaskURL+'scg/get_client_device_data',''); 
	HttpRequest('get','get_ap_device_data',window.flaskURL+'scg/get_ap_device_data',''); 

});
