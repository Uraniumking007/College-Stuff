# Practical 9: Basic Node.cjs Programs

This directory contains practical examples demonstrating fundamental Node.cjs concepts for backend development.

## Overview

Each example file demonstrates a different core concept of Node.cjs backend programming:

1. **01-basic-http-server.cjs** - Basic HTTP server using Node's built-in `http` module
2. **02-file-server.cjs** - Static file server with MIME type handling
3. **03-rest-api-server.cjs** - RESTful API with CRUD operations
4. **04-streams-example.cjs** - Reading/writing files using streams
5. **05-event-emitter.cjs** - Event-driven programming with EventEmitter

## Prerequisites

- Node.cjs installed (v14 or higher recommended)
- Basic understanding of JavaScript
- Terminal/command prompt access

## Running the Examples

Each example runs on a different port to avoid conflicts:

### 1. Basic HTTP Server (Port 3001)

```bash
cd backend/practical9
node 01-basic-http-server.cjs
```

**Features:**
- Route handling (/home, /about, /contact, /api)
- Custom 404 page
- Basic HTTP responses

**Test:**
```bash
curl http://localhost:3001/
```

### 2. File Server (Port 3002)

```bash
cd backend/practical9
node 02-file-server.cjs
```

**Features:**
- Serves static files
- Automatic MIME type detection
- Custom 404 for missing files

**Test:**
```bash
curl http://localhost:3002/index.html
```

### 3. REST API Server (Port 3003)

```bash
cd backend/practical9
node 03-rest-api-server.cjs
```

**Features:**
- GET all users: `GET /api/users`
- GET single user: `GET /api/users/:id`
- Create user: `POST /api/users`
- Update user: `PUT /api/users/:id`
- Delete user: `DELETE /api/users/:id`

**Test:**
```bash
# Get all users
curl http://localhost:3003/api/users

# Get single user
curl http://localhost:3003/api/users/1

# Create new user
curl -X POST http://localhost:3003/api/users \
  -H "Content-Type: application/json" \
  -d '{"name":"Alice","email":"alice@example.com"}'

# Update user
curl -X PUT http://localhost:3003/api/users/1 \
  -H "Content-Type: application/json" \
  -d '{"name":"John Updated","email":"john@example.com"}'

# Delete user
curl -X DELETE http://localhost:3003/api/users/1
```

### 4. Streams Example (Port 3004)

```bash
cd backend/practical9
node 04-streams-example.cjs
```

**Features:**
- Read streams (read file in chunks)
- Write streams (write data efficiently)
- Pipe streams (connect read to write)
- Memory-efficient file handling

**Test:**
```bash
curl http://localhost:3004/read-stream
curl http://localhost:3004/write-stream
curl http://localhost:3004/pipe-stream
```

### 5. Event Emitter (Port 3005)

```bash
cd backend/practical9
node 05-event-emitter.cjs
```

**Features:**
- Custom events
- Event listeners
- One-time listeners
- Error handling

**Test:**
```bash
curl http://localhost:3005/login    # Emits userLogin event
curl http://localhost:3005/logout   # Emits userLogout event
curl http://localhost:3005/error    # Emits error event
```

## Key Concepts Covered

### HTTP Module
- Creating servers without Express
- Request/response handling
- Routing basics
- Status codes and headers

### File System (fs)
- Reading files
- Writing files
- Serving static content
- MIME type handling

### REST API
- RESTful design principles
- CRUD operations
- JSON data handling
- Request parsing

### Streams
- Read streams
- Write streams
- Pipe operations
- Memory efficiency

### Event Emitter
- Event-driven architecture
- Custom events
- Event listeners
- Error handling

## Tips

1. **Stop servers:** Press `Ctrl+C` in the terminal to stop any running server

2. **Port conflicts:** If you get a "port already in use" error, either:
   - Stop the other process using that port
   - Change the PORT variable in the code

3. **Multiple servers:** You can run multiple examples simultaneously as they use different ports (3001-3005)

4. **Testing:** Use `curl`, Postman, or your browser to test the endpoints

5. **Logs:** Watch the terminal for server logs and event emissions

## Next Steps

After mastering these basics:
- Learn Express.cjs framework
- Explore database integration (MongoDB, PostgreSQL)
- Understand middleware concepts
- Learn about authentication
- Study error handling best practices

## Common Issues

**Issue:** `EADDRINUSE` error  
**Solution:** Another process is using the port. Stop it or use a different port.

**Issue:** `ENOENT` file not found  
**Solution:** Make sure you're running from the correct directory.

**Issue:** `EACCES` permission denied  
**Solution:** Check file permissions. Avoid running as root.

## Resources

- [Node.cjs Documentation](https://nodejs.org/docs)
- [HTTP Module](https://nodejs.org/api/http.html)
- [File System](https://nodejs.org/api/fs.html)
- [Streams](https://nodejs.org/api/stream.html)
- [Events](https://nodejs.org/api/events.html)
