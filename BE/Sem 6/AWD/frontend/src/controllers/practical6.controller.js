// Practical 6 Controller - Two-way data binding with validation
angular.module("app").controller("Practical6Controller", [
   "$scope",
   function($scope) {
      $scope.name = "";
      $scope.email = "";
      $scope.message = "";

      $scope.submitForm = function() {
         if ($scope.myForm.$valid) {
            alert(
               "Form Submitted Successfully!\n\nName: " +
               $scope.name +
               "\nEmail: " +
               $scope.email +
               "\nMessage: " +
               $scope.message,
            );
         }
      };

      $scope.resetForm = function() {
         $scope.name = "";
         $scope.email = "";
         $scope.message = "";
         if ($scope.myForm) {
            $scope.myForm.$setPristine();
            $scope.myForm.$setUntouched();
         }
      };
   },
]);
