// Practical 7 Controller - AngularJS modules and controllers with validation
angular.module("app").controller("Practical7Controller", [
   "$scope",
   function($scope) {
      $scope.name = "";
      $scope.email = "";
      $scope.password = "";
      $scope.confirmPassword = "";
      $scope.message = "";

      $scope.submitForm = function() {
         if ($scope.registerForm.$valid) {
            alert(
               "Registration Successful!\n\nName: " +
               $scope.name +
               "\nEmail: " +
               $scope.email +
               "\nMessage: " +
               ($scope.message || "No message"),
            );
         }
      };

      $scope.resetForm = function() {
         $scope.name = "";
         $scope.email = "";
         $scope.password = "";
         $scope.confirmPassword = "";
         $scope.message = "";
         if ($scope.registerForm) {
            $scope.registerForm.$setPristine();
            $scope.registerForm.$setUntouched();
         }
      };
   },
]);

// Note: compareTo directive is now in /src/directives/compareTo.directive.js