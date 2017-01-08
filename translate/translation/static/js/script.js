var app = angular.module('translateapp', [])

app.controller('TranslationsController',
    function($scope, $http, $httpParamSerializerJQLike) { 
        $scope.results = false;

        $scope.submit = function() {
            $scope.translateForm.$setPristine();
            $http({
                method: 'POST',
                url: '/translate/',
                data: $httpParamSerializerJQLike({text: $scope.translate.text, language: 'en'}),
                headers: {
                  'Content-Type': 'application/x-www-form-urlencoded'
                }
            })
            .then(function(response){
                console.log(response);
                $scope.results = true
                $scope.inputText = response.data.input;
                $scope.sourceLanguage = response.data.detectedSourceLanguage;
                $scope.translatedText = response.data.translatedText;
                $scope.targetLanguage = response.data.targetLanguage;
                
                //$scope.translateForm.$setUntouched();
            })
            .catch(function(error){
                console.error(error);
            })


        }
    }
)

app.directive('showResults', function(){
    return {
        restrict: 'E',
        template: '<h3>"{{inputText}}"</h3><p>translated from: {{sourceLanguage}}</p><h3>"{{translatedText}}"</h3><p>translated to: {{targetLanguage}}</p>'
    }
})

app.config([
    '$httpProvider', function($httpProvider) {
        $httpProvider.defaults.xsrfCookieName = 'csrftoken';
        $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    }
])