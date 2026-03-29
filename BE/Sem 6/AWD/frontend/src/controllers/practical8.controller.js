// Practical 8 Controller - Comprehensive form validation using AngularJS
angular.module("app").controller("Practical8Controller", [
   "$scope",
   function($scope) {
      // Initialize user object
      $scope.user = {
         name: "",
         email: "",
         phone: "",
         gender: "",
         password: "",
         confirmPassword: "",
         age: "",
      };
      $scope.submitForm = function() {
         if ($scope.validationForm.$valid) {
            // Build success message with all form data
            var message =
               "Form submitted successfully!\n\n" +
               "Name: " +
               $scope.user.name +
               "\n" +
               "Email: " +
               $scope.user.email +
               "\n";

            // Add phone if provided
            if ($scope.user.phone) {
               message += "Phone: " + $scope.user.phone + "\n";
            }

            // Add gender
            message += "Gender: " + $scope.user.gender + "\n";

            // Add age if provided
            if ($scope.user.age) {
               message += "Age: " + $scope.user.age + "\n";
            }

            // Show success alert
            alert(message);

            // Mark form as submitted
            $scope.validationForm.$submitted = true;

            console.log("Form submitted with data:", $scope.user);
         } else {
            // If form is invalid, mark all fields as touched to show errors
            angular.forEach($scope.validationForm.$error, function(field) {
               angular.forEach(field, function(errorField) {
                  errorField.$setTouched();
               });
            });

            console.log("Form is invalid. Please fix errors.");
         }
      };

      // Reset form handler
      $scope.resetForm = function() {
         // Reset user object
         $scope.user = {
            name: "",
            email: "",
            phone: "",
            gender: "",
            password: "",
            confirmPassword: "",
            age: "",
         };

         // Reset form state
         if ($scope.validationForm) {
            $scope.validationForm.$setPristine();
            $scope.validationForm.$setUntouched();
            $scope.validationForm.$submitted = false;
         }

         console.log("Form has been reset");
      };
   },
]);

// Note: compareTo directive is now in /src/directives/compareTo.directive.js