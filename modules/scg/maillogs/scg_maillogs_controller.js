window[appName].controller('scg_maillogs_controller',function($scope,$state,$http,$rootScope,$window){
	
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

case 'get_mail_logs':

$scope.scg_mail_log = response;

break;

}

}

HttpRequest('get','get_mail_logs',window.flaskURL+'scg/get_mail_logs',''); 


});
