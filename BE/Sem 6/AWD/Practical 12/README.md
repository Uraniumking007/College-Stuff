# Practical 12: Docker Todo Application

A simple full-stack Todo application demonstrating **Docker containerization** with frontend, backend, and database integration.

## 🎯 Objective

Develop a simple application integrating:
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Backend**: Express.js REST API
- **Database**: MongoDB
- **Containerization**: Docker & Docker Compose

## 🏗️ Architecture

```
┌─────────────┐      ┌─────────────┐      ┌─────────────┐
│  Frontend   │─────▶│   Backend   │─────▶│  MongoDB    │
│  (Node.js)  │      │ (Express)   │      │  Database   │
│  Port: 3000 │      │  Port: 5000 │      │  Port: 27017│
└─────────────┘      └─────────────┘      └─────────────┘
```

### Tech Stack

- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Backend**: Node.js, Express.js
- **Database**: MongoDB
- **Containerization**: Docker, Docker Compose
- **API Design**: RESTful API

## 📁 Project Structure

```
Practical 12/
├── backend/
│   ├── src/
│   │   ├── controllers/
│   │   │   └── todo.controller.js    # Business logic
│   │   ├── models/
│   │   │   └── Todo.js               # Mongoose model
│   │   ├── routes/
│   │   │   └── todo.routes.js        # API routes
│   │   └── server.js                 # Express server
│   ├── Dockerfile
│   ├── package.json
│   └── .dockerignore
├── frontend/
│   ├── src/
│   │   ├── css/
│   │   │   └── style.css             # Styling
│   │   ├── js/
│   │   │   └── app.js                # Frontend logic
│   │   └── index.html                # Main HTML
│   ├── Dockerfile
│   ├── package.json
│   └── .dockerignore
├── docker-compose.yml
└── README.md
```

## 🚀 Getting Started

### Prerequisites

- Docker Desktop installed and running
- Docker Compose (comes with Docker Desktop)

### Installation & Running

1. **Navigate to the project directory**:
   ```bash
   cd "Practical 12"
   ```

2. **Start all containers**:
   ```bash
   docker-compose up
   ```

3. **Access the application**:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:5000
   - MongoDB: mongodb://localhost:27017

4. **Stop the application**:
   - Press `Ctrl+C` in the terminal
   - Or run: `docker-compose down`

5. **Clean up everything** (remove containers and volumes):
   ```bash
   docker-compose down -v
   ```

## 📝 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/todos` | Get all todos |
| GET | `/api/todos/:id` | Get single todo |
| POST | `/api/todos` | Create new todo |
| PUT | `/api/todos/:id` | Update todo |
| PATCH | `/api/todos/:id/toggle` | Toggle completion |
| DELETE | `/api/todos/:id` | Delete todo |

### Example API Usage

**Create Todo**:
```bash
curl -X POST http://localhost:5000/api/todos \
  -H "Content-Type: application/json" \
  -d '{"text": "Learn Docker"}'
```

**Get All Todos**:
```bash
curl http://localhost:5000/api/todos
```

**Toggle Todo**:
```bash
curl -X PATCH http://localhost:5000/api/todos/<id>/toggle
```

**Delete Todo**:
```bash
curl -X DELETE http://localhost:5000/api/todos/<id>
```

## 🔧 Docker Commands

### Build Images
```bash
docker-compose build
```

### Start Services
```bash
docker-compose up
# Run in background
docker-compose up -d
```

### View Logs
```bash
# All services
docker-compose logs

# Specific service
docker-compose logs backend
docker-compose logs frontend
docker-compose logs mongo
```

### Stop Services
```bash
docker-compose stop
```

### Remove Containers
```bash
docker-compose down
```

### View Running Containers
```bash
docker-compose ps
```

## 🐳 Docker Concepts Demonstrated

1. **Containerization**: Each service runs in its own container
2. **Docker Compose**: Orchestrate multi-container applications
3. **Networking**: Services communicate via Docker network
4. **Volumes**: Persistent data storage for MongoDB
5. **Health Checks**: MongoDB health check for dependency management
6. **Environment Variables**: Configuration via environment variables

## 🎨 Features

- ✅ Create, read, update, and delete todos
- ✅ Mark todos as complete/incomplete
- ✅ Real-time statistics
- ✅ Responsive design
- ✅ Error handling
- ✅ Loading states
- ✅ Data persistence with MongoDB

## 🧪 Testing the Application

1. Open http://localhost:3000 in your browser
2. Add a new todo
3. Toggle todo completion by clicking the checkbox
4. Delete a todo
5. Check statistics update in real-time
6. Refresh the page to verify data persistence

## 📊 Container Details

### Backend Container
- **Base Image**: node:18-alpine
- **Port**: 5000
- **Dependencies**: Express, Mongoose, CORS
- **Environment**: MongoDB connection string

### Frontend Container
- **Base Image**: node:18-alpine
- **Port**: 3000
- **Server**: live-server
- **Static Files**: HTML, CSS, JS

### MongoDB Container
- **Image**: mongo:7.0
- **Port**: 27017
- **Volume**: mongo_data (persistent storage)

## 🔍 Troubleshooting

### Containers not starting
```bash
# Check container status
docker-compose ps

# View logs
docker-compose logs
```

### Port already in use
```bash
# Change ports in docker-compose.yml
ports:
  - "3001:3000"  # Use different port
```

### Database connection issues
- Ensure MongoDB container is healthy
- Check backend logs: `docker-compose logs backend`
- Verify MONGO_URI environment variable

## 📚 Learning Outcomes

After completing this practical, you should understand:
1. ✅ How to containerize a Node.js application
2. ✅ How to use Docker Compose for multi-container apps
3. ✅ How to implement RESTful APIs
4. ✅ How to connect frontend to backend via APIs
5. ✅ How to implement CRUD operations
6. ✅ How to use MongoDB with Mongoose
7. ✅ How to implement health checks
8. ✅ How to manage persistent data with volumes

## 🎓 Notes

- This is a practical demonstration of Docker in full-stack development
- Focus is on containerization, not on advanced features
- Can be extended with user authentication, categories, due dates, etc.
- Production deployment would require additional security measures

## 📝 License

This is an educational project for Advanced Web Development course.

---

**Course**: Advanced Web Development (Sem 6 - BE)  
**Practical**: 12  
**Topic**: Docker Integration - Frontend + Backend + Database
