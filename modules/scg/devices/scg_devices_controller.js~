window[appName].controller('scg_devices_controller',function($scope,$state,$http,$rootScope,$window){

//console.log("am inside");

function HttpRequest(method,action, URL, parameter) {
		
		$rootScope.showLoader = true;
		
        var $promise = '';
        if(method==="post") {
            $promise = $http.post(URL, parameter);
        } else {
            $promise = $http.get(URL, parameter);
        }
        $promise.then(function (response) {
            var result = angular.fromJson(response.data);
            processTheData(action, result);
			
			$rootScope.showLoader = false;
			
        });
    };

function processTheData(action, response) {
	
switch (action) {

case 'get_config_devices':

$scope.scg_device_list = response;

break;

}

}

HttpRequest('get','get_config_devices',window.flaskURL+'scg/get_config_devices',''); 

});
