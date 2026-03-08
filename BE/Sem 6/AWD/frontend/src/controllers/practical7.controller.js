angular.module("app").controller("Practical7Controller", [
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
          "\nPassword: " +
          $scope.password +
          $scope.message,
      );
    };
  },
]);
