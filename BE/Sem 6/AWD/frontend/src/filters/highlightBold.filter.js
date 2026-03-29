angular.module("app").filter("highlightBold", [
   function() {
      return function(input) {
         if (!input) {
            return "";
         }

         // If the input contains HTML tags, return as-is
         if (/<[^>]+>/.test(input)) {
            return input;
         }

         // Otherwise, wrap the entire text in <strong> tags
         return "<strong>" + input + "</strong>";
      };
   },
]);
