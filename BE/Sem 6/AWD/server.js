// Import the built-in HTTP module
const http = require("http");

// Define hostname and port
const hostname = "127.0.0.1";
const port = 3000;

// Create the server
const server = http.createServer((req, res) => {
  // Set response status and headers
  res.statusCode = 200;
  res.setHeader("Content-Type", "text/plain");

  // Send response
  res.end("Hello, World! 👋");
});

// Start the server
server.listen(port, hostname, () => {
  console.log(`Server running at http://${hostname}:${port}/`);
});
