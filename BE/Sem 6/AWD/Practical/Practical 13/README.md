# Practical 13: Basic HTTP Server using Node.js

## Objective
Create a basic HTTP server using Node.js built-in `http` module.

## Description
This practical demonstrates how to create a simple HTTP server using Node.js. The server can handle multiple routes and serve different content based on the URL path.

## Features
- Basic HTTP server using Node.js `http` module
- Multiple route handling:
  - `/` - Home page
  - `/about` - About page
  - `/contact` - Contact page
  - Any other path - 404 Not Found page
- HTML content serving
- Proper HTTP status codes (200, 404)

## How to Run

1. Navigate to the Practical 13 directory:
```bash
cd "Practical/Practical 13"
```

2. Run the server:
```bash
node server.js
```

OR using npm:
```bash
npm start
```

3. Open your browser and visit:
- http://127.0.0.1:3000/ - Home page
- http://127.0.0.1:3000/about - About page
- http://127.0.0.1:3000/contact - Contact page
- http://127.0.0.1:3000/anything - 404 page

4. To stop the server, press `Ctrl+C` in the terminal.

## Server Configuration
- Host: 127.0.0.1 (localhost)
- Port: 3000

## Code Explanation

1. **Import http module**: `const http = require('http');`
2. **Create server**: `http.createServer()` creates an HTTP server
3. **Handle requests**: The callback function processes incoming requests
4. **Route handling**: Check `req.url` to determine which page to serve
5. **Send response**: Use `res.end()` to send the response content
6. **Listen for connections**: `server.listen()` starts the server on specified port

## Requirements
- Node.js (no external dependencies required)
