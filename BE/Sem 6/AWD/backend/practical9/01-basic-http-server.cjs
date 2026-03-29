// 01-basic-http-server.js
// Basic HTTP Server using Node.js built-in http module

const http = require('http');

const PORT = 3001;

const server = http.createServer((req, res) => {
  console.log(`${new Date().toISOString()} - ${req.method} ${req.url}`);

  res.writeHead(200, { 'Content-Type': 'text/html' });

  if (req.url === '/' || req.url === '/home') {
    res.write('<h1>Welcome to Node.js HTTP Server</h1>');
    res.write('<p>This is a basic HTTP server without Express!</p>');
    res.write('<ul>');
    res.write('<li><a href="/about">About</a></li>');
    res.write('<li><a href="/contact">Contact</a></li>');
    res.write('<li><a href="/api">API</a></li>');
    res.write('</ul>');
  } else if (req.url === '/about') {
    res.write('<h1>About Page</h1>');
    res.write('<p>This is a simple HTTP server built with Node.js</p>');
    res.write('<p><a href="/">Back to Home</a></p>');
  } else if (req.url === '/contact') {
    res.write('<h1>Contact Page</h1>');
    res.write('<p>Email: test@example.com</p>');
    res.write('<p><a href="/">Back to Home</a></p>');
  } else if (req.url === '/api') {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.write(JSON.stringify({
      message: 'API endpoint',
      version: '1.0.0',
      endpoints: ['/api/users', '/api/posts', '/api/status']
    }));
  } else {
    res.writeHead(404, { 'Content-Type': 'text/html' });
    res.write('<h1>404 - Page Not Found</h1>');
    res.write('<p><a href="/">Back to Home</a></p>');
  }

  res.end();
});

server.listen(PORT, () => {
  console.log('Basic HTTP Server Started');
  console.log(`Server running at: http://localhost:${PORT}/`);
  console.log('\nAvailable routes:');
  console.log(`  - http://localhost:${PORT}/`);
  console.log(`  - http://localhost:${PORT}/about`);
  console.log(`  - http://localhost:${PORT}/contact`);
  console.log(`  - http://localhost:${PORT}/api`);
  console.log('\nPress Ctrl+C to stop the server\n');
});

server.on('error', (err) => {
  if (err.code === 'EADDRINUSE') {
    console.error(`Port ${PORT} is already in use!`);
  } else {
    console.error('Server error:', err);
  }
  process.exit(1);
});
