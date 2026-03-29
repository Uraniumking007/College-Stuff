// 05-event-emitter.js
// Event Emitter - Event-driven programming in Node.js

const http = require('http');
const EventEmitter = require('events');

const PORT = 3005;

// Create a custom event emitter
class MyEmitter extends EventEmitter {}

const myEmitter = new MyEmitter();

// Event listeners
myEmitter.on('userLogin', (user) => {
  console.log(`✅ User logged in: ${user.name} at ${new Date().toISOString()}`);
});

myEmitter.on('userLogout', (user) => {
  console.log(`👋 User logged out: ${user.name} at ${new Date().toISOString()}`);
});

myEmitter.on('error', (err) => {
  console.error(`❌ Error occurred: ${err.message}`);
});

// One-time listener
myEmitter.once('serverStart', () => {
  console.log('🚀 Server started (this will only be logged once)');
});

const server = http.createServer((req, res) => {
  console.log(`${req.method} ${req.url}`);

  res.writeHead(200, { 'Content-Type': 'text/html' });

  if (req.url === '/' || req.url === '/home') {
    // Emit serverStart event (only fires once due to .once())
    myEmitter.emit('serverStart');

    res.end(`
      <h1>Event Emitter Example</h1>
      <p>Event-driven programming with Node.js EventEmitter</p>
      <h2>Available Actions:</h2>
      <ul>
        <li><a href="/login">Simulate User Login</a></li>
        <li><a href="/logout">Simulate User Logout</a></li>
        <li><a href="/error">Simulate Error</a></li>
      </ul>
      <p><em>Check the server console to see events being emitted!</em></p>
    `);

  } else if (req.url === '/login') {
    const user = { id: 1, name: 'John Doe', email: 'john@example.com' };
    
    // Emit userLogin event
    myEmitter.emit('userLogin', user);

    res.end(`
      <h1>User Login Event</h1>
      <p>Emitted 'userLogin' event with user data:</p>
      <pre>${JSON.stringify(user, null, 2)}</pre>
      <p>Check server console for the event log!</p>
      <p><a href="/">Back to Home</a></p>
    `);

  } else if (req.url === '/logout') {
    const user = { id: 1, name: 'John Doe', email: 'john@example.com' };
    
    // Emit userLogout event
    myEmitter.emit('userLogout', user);

    res.end(`
      <h1>User Logout Event</h1>
      <p>Emitted 'userLogout' event with user data:</p>
      <pre>${JSON.stringify(user, null, 2)}</pre>
      <p>Check server console for the event log!</p>
      <p><a href="/">Back to Home</a></p>
    `);

  } else if (req.url === '/error') {
    const error = new Error('This is a simulated error!');
    
    // Emit error event
    myEmitter.emit('error', error);

    res.end(`
      <h1>Error Event</h1>
      <p>Emitted 'error' event:</p>
      <pre>${error.message}</pre>
      <p>Check server console for the error log!</p>
      <p><a href="/">Back to Home</a></p>
    `);

  } else {
    res.writeHead(404, { 'Content-Type': 'text/html' });
    res.end('<h1>404 - Page Not Found</h1><p><a href="/">Back to Home</a></p>');
  }
});

server.listen(PORT, () => {
  console.log('Event Emitter Server Started');
  console.log(`Server running at: http://localhost:${PORT}/`);
  console.log('\nAvailable routes:');
  console.log('  - /');
  console.log('  - /login (emits userLogin event)');
  console.log('  - /logout (emits userLogout event)');
  console.log('  - /error (emits error event)');
  console.log('\nPress Ctrl+C to stop the server\n');
});
