// Practical 6 Controller - Two-way data binding
angular.module("app").controller("Practical6Controller", [
  "$scope",
  function ($scope) {
    $scope.name = "";
    $scope.email = "";
    $scope.message = "";

    $scope.submitForm = function () {
      alert(
        "Form Submitted!\nName: " +
          $scope.name +
          "\nEmail: " +
          $scope.email +
          "\nMessage: " +
          $scope.message,
      );
    };
  },
]);
