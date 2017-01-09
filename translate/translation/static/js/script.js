var app = angular.module('translateapp', [])

app.controller('TranslationsController',
    function($scope, $http, $httpParamSerializerJQLike) {
        $scope.results = false;

        //
        // $scope.results = true
        // $scope.inputText = 'the inputText';
        // $scope.detectedLanguageName = 'the sourceLanguageName';
        // $scope.detectedLanguageCode = 'the sourceLanguageCode';
        // $scope.translatedText = 'the translatedText';
        // $scope.targetLanguageName = 'the targetLanguageName';
        // $scope.targetLanguageCode = 'the targetLanguageCode';
        //

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
                $scope.input_dict = response.data.input_text;
                $scope.translated_dict = response.data.translated_text;

                $scope.inputText = $scope.input_dict.text;
                $scope.detectedLanguageName = $scope.input_dict.language_name;
                $scope.detectedLanguageCode = $scope.input_dict.language_code;

                $scope.translatedText = $scope.translated_dict.text;
                $scope.targetLanguageName = $scope.translated_dict.language_name;
                $scope.targetLanguageCode = $scope.translated_dict.language_code;
                
                //$scope.translateForm.$setUntouched();
            })
            .catch(function(error){
                console.error(error);
            })
        }

        $scope.loadTranslations = function(){
            $http({
                    method: 'GET',
                    url: '/translations/',
                    headers: {
                      'Accept': 'application/json'
                    }
            })
            .then(function(response){
                console.log(response);
            })
        }
        // call this function on page load
        $scope.loadTranslations();
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