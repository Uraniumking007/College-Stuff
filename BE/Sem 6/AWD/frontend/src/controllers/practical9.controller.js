// Practical 9 Controller - Basic Node.js Programs
angular.module("app").controller("Practical9Controller", [
   "$scope",
   function($scope) {
      // Initialize scope variables
      $scope.practicalTitle = "Practical 9 - Basic Node.js Programs";
      $scope.practicalDescription =
         "Demonstrating basic Node.js programs and how to execute them";

      // Node.js examples data
      $scope.nodeExamples = {
         helloWorld: {
            title: "Hello World",
            description: "The simplest Node.js program - console output",
            code: `// hello.js
console.log("Hello, World!");
console.log("Welcome to Node.js");`,
            output: "Hello, World!\nWelcome to Node.js",
            runCommand: "node hello.js",
         },
         arithmetic: {
            title: "Basic Arithmetic",
            description: "Performing mathematical calculations",
            code: `// arithmetic.js
let a = 10;
let b = 5;
console.log("Addition:", a + b);`,
            output: "Addition: 15",
            runCommand: "node arithmetic.js",
         },
      };

      // Log controller initialization
      console.log("Practical9Controller loaded");
      console.log("Practical:", $scope.practicalTitle);
   },
]);
