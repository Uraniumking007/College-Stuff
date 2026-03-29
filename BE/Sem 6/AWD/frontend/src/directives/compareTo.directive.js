// Custom directive for password confirmation comparison
// This file should only be loaded once to prevent $compile:multidir errors
angular.module('app').directive('compareTo', function() {
   return {
      require: 'ngModel',
      scope: {
         otherModelValue: '=compareTo',
      },
      link: function(scope, element, attributes, ngModel) {
         ngModel.$validators.compareTo = function(modelValue) {
            // Only validate if both values have content
            if (!modelValue || !scope.otherModelValue) {
               return true; // Don't show mismatch error while typing
            }
            return modelValue === scope.otherModelValue;
         };

         scope.$watch('otherModelValue', function() {
            ngModel.$validate();
         });
      },
   };
});
