// AngularJS 1.8.2 Application
angular
   .module("app", ["ngRoute"])

   // Configure routes
   .config([
      "$routeProvider",
      "$locationProvider",
      function($routeProvider, $locationProvider) {
         $routeProvider
            .when("/", {
               templateUrl: "/views/home.html",
               controller: "MainController",
            })
            .when("/practical6", {
               templateUrl: "/views/practical6.html",
               controller: "Practical6Controller",
            })
            .when("/practical7", {
               templateUrl: "/views/practical7.html",
               controller: "Practical7Controller",
            })
            .when("/practical8", {
               templateUrl: "/views/practical8.html",
               controller: "Practical8Controller",
            })
            .when("/practical9", {
               templateUrl: "/views/practical9.html",
               controller: "Practical9Controller",
            })
            .when("/practical10", {
               templateUrl: "/views/practical10.html",
               controller: "Practical10Controller",
            })
            .otherwise({
               redirectTo: "/",
            });

         // Use hash mode for Vite compatibility (HTML5 mode requires server config)
         $locationProvider.html5Mode(false);
         $locationProvider.hashPrefix("");
      },
   ])

   .run([
      "$rootScope",
      "$location",
      function($rootScope, $location) {
         console.log("Angular app is running");
         console.log("Current path:", $location.path());

         // Log route changes
         $rootScope.$on("$routeChangeStart", function(event, next, current) {
            console.log(
               "Route changing from:",
               current ? current.templateUrl : "none",
            );
            console.log("Route changing to:", next.templateUrl);
         });

         $rootScope.$on(
            "$routeChangeError",
            function(event, current, previous, rejection) {
               console.error("Route change error:", rejection);
            },
         );

         $rootScope.$on(
            "$routeChangeSuccess",
            function(event, current, previous) {
               console.log(
                  "Route change successful:",
                  current ? current.templateUrl : "none",
               );
            },
         );
      },
   ]);
