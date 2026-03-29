angular.module("app").controller("Practical12Controller", [
   "$scope",
   "$http",
   "$window",
   function($scope, $http, $window) {
      $scope.title = "Practical 12: Dockerized Full-Stack Application";
      $scope.subtitle = "Student Management System with Docker Integration";

      $scope.students = [];
      $scope.currentStudent = {};
      $scope.isEditing = false;
      $scope.loading = false;
      $scope.error = null;
      $scope.successMessage = null;

      // API Base URL
      const API_URL = "/api/students";

      // Load all students
      $scope.loadStudents = function() {
         $scope.loading = true;
         $scope.error = null;

         $http
            .get(API_URL)
            .then(function(response) {
               $scope.students = response.data.data;
               $scope.loading = false;
            })
            .catch(function(error) {
               $scope.error = "Failed to load students: " + (error.data?.message || error.message);
               $scope.loading = false;
            });
      };

      // Save student (create or update)
      $scope.saveStudent = function() {
         if (!$scope.studentForm.$valid) {
            $scope.error = "Please fill all required fields correctly.";
            return;
         }

         $scope.loading = true;
         $scope.error = null;

         const request = $scope.isEditing
            ? $http.put(API_URL + "/" + $scope.currentStudent._id, $scope.currentStudent)
            : $http.post(API_URL, $scope.currentStudent);

         request
            .then(function(response) {
               $scope.successMessage = response.data.message;
               $scope.clearForm();
               $scope.loadStudents();

               // Clear success message after 3 seconds
               setTimeout(function() {
                  $scope.successMessage = null;
                  $scope.$apply();
               }, 3000);
            })
            .catch(function(error) {
               $scope.error = "Failed to save student: " + (error.data?.message || error.message);
               $scope.loading = false;
            });
      };

      // Edit student
      $scope.editStudent = function(student) {
         $scope.currentStudent = angular.copy(student);
         $scope.isEditing = true;
         $scope.error = null;
         $window.scrollTo(0, 0);
      };

      // Delete student
      $scope.deleteStudent = function(id) {
         if (!confirm("Are you sure you want to delete this student?")) {
            return;
         }

         $scope.loading = true;
         $scope.error = null;

         $http
            .delete(API_URL + "/" + id)
            .then(function(response) {
               $scope.successMessage = response.data.message;
               $scope.loadStudents();

               // Clear success message after 3 seconds
               setTimeout(function() {
                  $scope.successMessage = null;
                  $scope.$apply();
               }, 3000);
            })
            .catch(function(error) {
               $scope.error = "Failed to delete student: " + (error.data?.message || error.message);
               $scope.loading = false;
            });
      };

      // Clear form
      $scope.clearForm = function() {
         $scope.currentStudent = {};
         $scope.isEditing = false;
         $scope.error = null;
         if ($scope.studentForm) {
            $scope.studentForm.$setPristine();
            $scope.studentForm.$setUntouched();
         }
      };

      // Check Docker status
      $scope.checkDockerStatus = function() {
         $scope.loading = true;

         $http
            .get("/api/health")
            .then(function(response) {
               $scope.dockerStatus = {
                  backend: "Running",
                  database: response.data.mongodb === "connected" ? "Connected" : "Disconnected",
                  status: "success"
               };
               $scope.loading = false;
            })
            .catch(function(error) {
               $scope.dockerStatus = {
                  backend: "Error",
                  database: "Unknown",
                  status: "error",
                  message: "Cannot connect to backend"
               };
               $scope.loading = false;
            });
      };

      // Initialize
      $scope.loadStudents();
      $scope.checkDockerStatus();
   },
]);
