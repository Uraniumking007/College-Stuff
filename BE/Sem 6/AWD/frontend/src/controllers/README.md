# Controllers Directory

This directory contains all AngularJS controllers for the application.

## File Structure

```
controllers/
├── home.controller.js       # Main/Home page controller
├── practical6.controller.js # Practical 6 form controller
└── ...                      # Add more controllers as needed
```

## How to Add a New Controller

### 1. Create a new file in this directory

Example: `myview.controller.js`

```javascript
// MyView Controller
angular.module("app").controller("MyViewController", [
  "$scope",
  function ($scope) {
    // Your controller logic here
    $scope.message = "Hello from MyView!";
  },
]);
```

### 2. Register the controller in `app.js`

Add a new route in the `$routeProvider` config:

```javascript
.when("/myview", {
  templateUrl: "/views/myview.html",
  controller: "MyViewController",
})
```

### 3. Add the script to `index.html`

Add this line after the other controller scripts:

```html
<script src="/src/controllers/myview.controller.js"></script>
```

### 4. Create the view template

Create `public/views/myview.html`:

```html
<div class="container">
  <h1>{{ message }}</h1>
</div>
```

## Naming Convention

- Controller files: `{viewname}.controller.js`
- Controller names: `{Viewname}Controller` (PascalCase)
- Route paths: `/{viewname}` (lowercase)

## Dependencies

If your controller needs additional Angular services, inject them:

```javascript
angular.module("app").controller("MyController", [
  "$scope",
  "$http",
  "$location",
  function ($scope, $http, $location) {
    // Use injected services
    $http.get("/api/data").then(function(response) {
      $scope.data = response.data;
    });
  },
]);
```
