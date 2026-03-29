# Practical 9 - Run Steps

This document provides step-by-step instructions to run Practical 9 in both Backend and Frontend.

---

## 📁 Table of Contents

1. [Backend Practical 9](#backend-practical-9)
2. [Frontend Practical 9](#frontend-practical-9)
3. [Troubleshooting](#troubleshooting)

---

## 🔧 Backend Practical 9

### Overview
Backend Practical 9 demonstrates fundamental Node.js concepts for backend development including HTTP servers, file handling, REST APIs, streams, and event-driven programming.

### Location
`/backend/practical9/`

### Files Available
1. `01-basic-http-server.cjs` - Basic HTTP server with routing (Port 3001)
2. `02-file-server.cjs` - Static file server with MIME types (Port 3002)
3. `03-rest-api-server.cjs` - RESTful API with CRUD operations (Port 3003)
4. `04-streams-example.cjs` - File read/write streams (Port 3004)
5. `05-event-emitter.cjs` - Event-driven programming (Port 3005)

### Prerequisites
- Node.js installed (v14 or higher recommended)
- Terminal/command prompt access
- Basic understanding of JavaScript

### Steps to Run Backend Examples

#### Step 1: Open Terminal
Open your terminal or command prompt.

#### Step 2: Navigate to Backend Directory
```bash
cd /Users/bhaveshpatil/Documents/github/College-Stuff/BE/Sem\ 6/AWD/backend/practical9
```

#### Step 3: Run Individual Examples

**1. Basic HTTP Server (Port 3001)**
```bash
node 01-basic-http-server.cjs
```
- Features: Route handling (/home, /about, /contact, /api), custom 404 page
- Test in browser: http://localhost:3001/
- Test with curl: `curl http://localhost:3001/`

**2. File Server (Port 3002)**
```bash
node 02-file-server.cjs
```
- Features: Serves static files, automatic MIME type detection
- Test in browser: http://localhost:3002/index.html
- Test with curl: `curl http://localhost:3002/index.html`

**3. REST API Server (Port 3003)**
```bash
node 03-rest-api-server.cjs
```
- Features: Full CRUD operations for user management
- Test with curl:
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

**4. Streams Example (Port 3004)**
```bash
node 04-streams-example.cjs
```
- Features: Read streams, write streams, pipe operations
- Test with curl:
  ```bash
  curl http://localhost:3004/read-stream
  curl http://localhost:3004/write-stream
  curl http://localhost:3004/pipe-stream
  ```

**5. Event Emitter (Port 3005)**
```bash
node 05-event-emitter.cjs
```
- Features: Custom events, event listeners, error handling
- Test with curl:
  ```bash
  curl http://localhost:3005/login    # Emits userLogin event
  curl http://localhost:3005/logout   # Emits userLogout event
  curl http://localhost:3005/error    # Emits error event
  ```

#### Step 4: Stop Servers
Press `Ctrl+C` in the terminal to stop any running server.

### Important Notes
- Each example runs on a different port (3001-3005) to avoid conflicts
- You can run multiple examples simultaneously in separate terminals
- Watch the terminal for server logs and event emissions
- Use browser, curl, or Postman for testing

---

## 🌐 Frontend Practical 9

### Overview
Frontend Practical 9 is an AngularJS-based web application that demonstrates and explains basic Node.js programs through an interactive web interface.

### Location
- Controller: `/frontend/src/controllers/practical9.controller.js`
- View: `/frontend/public/views/practical9.html`

### Prerequisites
- Node.js installed
- AngularJS application running
- Backend server running (if applicable)

### Steps to Run Frontend Practical 9

#### Step 1: Start the Frontend Application

**Option A: Using Bun (Recommended)**
```bash
cd /Users/bhaveshpatil/Documents/github/College-Stuff/BE/Sem\ 6/AWD
bun run dev
```

**Option B: Using npm**
```bash
cd /Users/bhaveshpatil/Documents/github/College-Stuff/BE/Sem\ 6/AWD
npm run dev
```

#### Step 2: Access the Application
Once the development server starts:
1. Open your web browser
2. Navigate to the URL shown in terminal (typically http://localhost:5173 or similar)

#### Step 3: Navigate to Practical 9
1. Look for a navigation menu or link to "Practical 9"
2. Click on the Practical 9 link
3. The page will display:
   - Introduction to Node.js
   - Multiple code examples with explanations
   - Expected output for each example
   - Instructions on how to run each program

### Examples Demonstrated in Frontend
The frontend displays the following Node.js examples:

1. **Hello World** - Basic console output
2. **Basic Arithmetic** - Mathematical operations
3. **Working with Arrays** - Array methods and operations
4. **Functions** - Function declarations and expressions
5. **File System Operations** - Reading and writing files
6. **Simple HTTP Server** - Creating a web server
7. **Module System** - Importing and exporting modules

### Features of Frontend Practical 9
- Interactive code examples with syntax highlighting
- Expected output display for each example
- Step-by-step instructions
- Responsive Bootstrap-based UI
- Clean, organized presentation

---

## 🛠️ Troubleshooting

### Common Backend Issues

**Issue: `EADDRINUSE` error (Port already in use)**
```bash
# Solution 1: Find and kill the process using the port
lsof -ti:3001 | xargs kill -9  # For port 3001

# Solution 2: Change the PORT variable in the code
```

**Issue: `ENOENT` file not found**
- Make sure you're running from the correct directory
- Check that the file exists in `/backend/practical9/`

**Issue: `EACCES` permission denied**
- Check file permissions
- Avoid running as root/sudo unless necessary

**Issue: Module not found**
```bash
cd backend
npm install
```

### Common Frontend Issues

**Issue: Development server won't start**
```bash
# Clear cache and reinstall dependencies
rm -rf node_modules
rm bun.lockb
bun install
```

**Issue: Browser shows blank page**
- Check browser console for errors (F12 → Console)
- Verify the dev server is running
- Try clearing browser cache

**Issue: Practical 9 page not found**
- Verify files exist:
  - `/frontend/public/views/practical9.html`
  - `/frontend/src/controllers/practical9.controller.js`
- Check that routing is properly configured in the Angular app

**Issue: Styles not loading**
- Ensure Bootstrap CDN is accessible
- Check browser console for network errors

---

## 📚 Additional Resources

### Backend
- [Node.js Documentation](https://nodejs.org/docs)
- [HTTP Module](https://nodejs.org/api/http.html)
- [File System](https://nodejs.org/api/fs.html)
- [Streams](https://nodejs.org/api/stream.html)
- [Events](https://nodejs.org/api/events.html)

### Frontend
- [AngularJS Documentation](https://angularjs.org/)
- [Bootstrap Documentation](https://getbootstrap.com/docs/)
- [JavaScript MDN](https://developer.mozilla.org/en-US/docs/Web/JavaScript)

---

## 🎯 Key Learning Outcomes

After completing Practical 9, you should understand:

### Backend
- How to create HTTP servers without frameworks
- File system operations in Node.js
- RESTful API design and implementation
- Stream-based file handling
- Event-driven programming patterns

### Frontend
- How to present Node.js concepts through a web interface
- AngularJS controller and view structure
- Interactive code documentation
- User-friendly tutorial design

---

## 💡 Tips for Success

1. **Start Simple**: Begin with the basic HTTP server, then progress to more complex examples
2. **Experiment**: Modify the code and see what happens
3. **Test Thoroughly**: Use different endpoints and inputs to understand behavior
4. **Read Logs**: Pay attention to console output for debugging
5. **Take Notes**: Document what you learn for future reference
6. **Ask Questions**: Don't hesitate to seek clarification on concepts

---

**Last Updated**: March 2026  
**Course**: Advanced Web Development (Sem 6)  
**Instructor**: [Your Instructor's Name]
