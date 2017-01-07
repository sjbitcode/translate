var app = angular.module('translateapp', [])

app.controller('TranslateEventController',
    function($scope) {
        $scope.firstName = 'Coffeemug';
        $scope.translations = [
            {username: 'bjorn', hometown: 'kattegat'},
            {username: 'ragnar', hometown: 'norway'},
            {username: 'lagertha', hometown: 'somewhere else'},
            {username: 'ecbert', hometown: 'england'}
        ]
    }
)

app.controller('TranslationsController',
    function($scope, $http) {
        $http({
                method: 'GET',
                url: 'http://127.0.0.1:9000/languages/'
            })
            .then(function(response){
                $scope.myData = response.data
            })
    }
)

app.directive('myCoolDirective', function(){
    return {
        restrict: 'EC',
        template: '<h1>YOOOO WASSUP</h1>'
    };
});

app.config([
    '$httpProvider', function($httpProvider) {
        $httpProvider.defaults.xsrfCookieName = 'csrftoken';
        $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    }
])