// AngularJS 1.8.2 Application
const app = angular.module('app', ['ngRoute']);

// Main Controller
app.controller('MainController', [
    '$scope', '$http', '$window',
    function ($scope, $http, $window) {
        // Initialize scope variables
        $scope.items = [];
        $scope.newItem = '';
        $scope.loading = true;
        $scope.error = null;

        const API_URL = '/api/items';

        // Fetch all items
        $scope.fetchItems = function () {
            $scope.loading = true;
            $scope.error = null;

            $http.get(API_URL)
                .then(function (response) {
                    $scope.items = response.data;
                    $scope.loading = false;
                })
                .catch(function (err) {
                    $scope.error = 'Failed to load items. Is the backend running?';
                    $scope.loading = false;
                    console.error('Error fetching items:', err);
                });
        };

        // Add new item
        $scope.addItem = function () {
            if (!$scope.newItem.trim()) return;

            $http.post(API_URL, { name: $scope.newItem })
                .then(function (response) {
                    $scope.items.push(response.data);
                    $scope.newItem = '';
                })
                .catch(function (err) {
                    $scope.error = 'Failed to add item';
                    console.error('Error adding item:', err);
                });
        };

        // Delete item
        $scope.deleteItem = function (id) {
            $http.delete(API_URL + '/' + id)
                .then(function (response) {
                    $scope.items = $scope.items.filter(function (item) {
                        return item._id !== id;
                    });
                })
                .catch(function (err) {
                    $scope.error = 'Failed to delete item';
                    console.error('Error deleting item:', err);
                });
        };

        // Load items on controller initialization
        $scope.fetchItems();
    }
]);

// Configure routes
app.config([
    '$routeProvider',
    '$locationProvider',
    function ($routeProvider, $locationProvider) {
        $routeProvider
            .when('/', {
                templateUrl: '/src/views/home.html',
                controller: 'MainController'
            })
            .otherwise({
                redirectTo: '/'
            });

        // Enable HTML5 mode (requires server configuration)
        $locationProvider.html5Mode(true);
    }
]);
