// Home Controller
angular.module("app").controller("MainController", [
  "$scope",
  function ($scope) {
    // Initialize scope variables
    $scope.message = "Welcome to the application";
    console.log("MainController loaded");
  },
]);
