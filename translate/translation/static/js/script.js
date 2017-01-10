var app = angular.module('translateapp', [])

app.controller('TranslationsController',
    function($scope, $http, $httpParamSerializerJQLike) {
        // lets us know if api translate call was made
        $scope.results = false;

        $scope.submit = function() {
            $scope.translateForm.$setPristine();
            $http({
                method: 'POST',
                url: '/api/translate/',
                data: $httpParamSerializerJQLike({text: $scope.translate.text, language: 'en'}),
                headers: {
                  'Content-Type': 'application/x-www-form-urlencoded'
                }
            })
            .then(function(response){
                // console.log(response);
                $scope.results = true
                $scope.input_dict = response.data.input_text;
                $scope.translated_dict = response.data.translated_text;

                $scope.inputText = $scope.input_dict.text;
                $scope.detectedLanguageName = $scope.input_dict.language_name;
                $scope.detectedLanguageCode = $scope.input_dict.language_code;

                $scope.translatedText = $scope.translated_dict.text;
                $scope.targetLanguageName = $scope.translated_dict.language_name;
                $scope.targetLanguageCode = $scope.translated_dict.language_code;
                
                // add new row and delete last to maintain latest 20 translations.
                $scope.insertRow(response.data);
                $scope.deleteLastRow();

                // $scope.translateForm.$setUntouched();
            })
            .catch(function(error){
                console.error(error);
                alert('Something went wrong!');
            })
        }

        $scope.insertRow = function(obj) {
            // insert row
            $scope.translation_events.unshift(obj);
            console.log($scope.translation_events);
        }

        $scope.deleteLastRow = function() {
            // delete last row
            $scope.translation_events.pop();
        }

        $scope.loadTranslations = function(){
            // make api call to /translations/ and apply ordering to get latest translation events.
            $http({
                    method: 'GET',
                    url: '/api/translations/?ordering=-created_on',
                    headers: {
                      'Accept': 'application/json'
                    }
            })
            .then(function(response) {
                // to be populated in table.
                $scope.translation_events = response.data.results;
            })
        }
        // call this function on page load
        $scope.loadTranslations();
    }
)

app.directive('showResults', function(){
    return {
        restrict: 'E',
        template: '<h3>"{{inputText}}"</h3><p>translated from: {{ detectedLanguageName }}</p><h3>"{{ translatedText }}"</h3><p>translated to: {{ targetLanguageName }}</p>'
    }
})

app.config([
    '$httpProvider', function($httpProvider) {
        $httpProvider.defaults.xsrfCookieName = 'csrftoken';
        $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    }
])