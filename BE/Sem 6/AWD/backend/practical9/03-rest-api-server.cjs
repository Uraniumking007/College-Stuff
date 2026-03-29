// 03-rest-api-server.js
// REST API Server - Simple RESTful API implementation

const http = require('http');
const url = require('url');

const PORT = 3003;

// In-memory data store
let users = [
  { id: 1, name: 'John Doe', email: 'john@example.com' },
  { id: 2, name: 'Jane Smith', email: 'jane@example.com' },
  { id: 3, name: 'Bob Johnson', email: 'bob@example.com' }
];

let nextId = 4;

const server = http.createServer((req, res) => {
  const parsedUrl = url.parse(req.url, true);
  const path = parsedUrl.pathname;
  const method = req.method;

  console.log(`${method} ${path}`);

  // Set JSON content type for all responses
  res.setHeader('Content-Type', 'application/json');

  // GET /api/users - Get all users
  if (path === '/api/users' && method === 'GET') {
    res.writeHead(200);
    res.end(JSON.stringify({
      success: true,
      count: users.length,
      data: users
    }));

  // GET /api/users/:id - Get single user
  } else if (path.startsWith('/api/users/') && method === 'GET') {
    const id = parseInt(path.split('/')[3]);
    const user = users.find(u => u.id === id);

    if (user) {
      res.writeHead(200);
      res.end(JSON.stringify({ success: true, data: user }));
    } else {
      res.writeHead(404);
      res.end(JSON.stringify({ success: false, message: 'User not found' }));
    }

  // POST /api/users - Create new user
  } else if (path === '/api/users' && method === 'POST') {
    let body = '';
    req.on('data', chunk => {
      body += chunk.toString();
    });
    req.on('end', () => {
      try {
        const { name, email } = JSON.parse(body);
        const newUser = { id: nextId++, name, email };
        users.push(newUser);

        res.writeHead(201);
        res.end(JSON.stringify({ success: true, data: newUser }));
      } catch (error) {
        res.writeHead(400);
        res.end(JSON.stringify({ success: false, message: 'Invalid JSON' }));
      }
    });

  // PUT /api/users/:id - Update user
  } else if (path.startsWith('/api/users/') && method === 'PUT') {
    const id = parseInt(path.split('/')[3]);
    const userIndex = users.findIndex(u => u.id === id);

    if (userIndex !== -1) {
      let body = '';
      req.on('data', chunk => {
        body += chunk.toString();
      });
      req.on('end', () => {
        try {
          const { name, email } = JSON.parse(body);
          users[userIndex] = { ...users[userIndex], name, email };

          res.writeHead(200);
          res.end(JSON.stringify({ success: true, data: users[userIndex] }));
        } catch (error) {
          res.writeHead(400);
          res.end(JSON.stringify({ success: false, message: 'Invalid JSON' }));
        }
      });
    } else {
      res.writeHead(404);
      res.end(JSON.stringify({ success: false, message: 'User not found' }));
    }

  // DELETE /api/users/:id - Delete user
  } else if (path.startsWith('/api/users/') && method === 'DELETE') {
    const id = parseInt(path.split('/')[3]);
    const userIndex = users.findIndex(u => u.id === id);

    if (userIndex !== -1) {
      users.splice(userIndex, 1);
      res.writeHead(200);
      res.end(JSON.stringify({ success: true, message: 'User deleted' }));
    } else {
      res.writeHead(404);
      res.end(JSON.stringify({ success: false, message: 'User not found' }));
    }

  // 404 for unknown routes
  } else {
    res.writeHead(404);
    res.end(JSON.stringify({ success: false, message: 'Route not found' }));
  }
});

server.listen(PORT, () => {
  console.log('REST API Server Started');
  console.log(`API server running at: http://localhost:${PORT}/`);
  console.log('\nAvailable endpoints:');
  console.log('  GET    /api/users       - Get all users');
  console.log('  GET    /api/users/:id   - Get single user');
  console.log('  POST   /api/users       - Create user');
  console.log('  PUT    /api/users/:id   - Update user');
  console.log('  DELETE /api/users/:id   - Delete user');
  console.log('\nExample: curl http://localhost:3003/api/users');
  console.log('\nPress Ctrl+C to stop the server\n');
});
