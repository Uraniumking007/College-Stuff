const http = require('http');

const hostname = '127.0.0.1';
const port = 3000;

const server = http.createServer((req, res) => {
   res.statusCode = 200;
   res.setHeader('Content-Type', 'text/html');

   if (req.url === '/') {
      res.end('<h1>Welcome to Node.js HTTP Server</h1><p>This is Practical 13</p>');
   } else if (req.url === '/about') {
      res.end('<h1>About Page</h1><p>Basic HTTP Server using Node.js</p>');
   } else if (req.url === '/contact') {
      res.end('<h1>Contact Page</h1><p>Email: test@example.com</p>');
   } else {
      res.statusCode = 404;
      res.end('<h1>404 - Page Not Found</h1>');
   }
});

server.listen(port, hostname, () => {
   console.log(`Server running at http://${hostname}:${port}/`);
   console.log('Press Ctrl+C to stop the server');
});
