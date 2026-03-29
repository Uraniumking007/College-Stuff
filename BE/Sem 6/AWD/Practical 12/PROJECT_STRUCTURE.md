# Practical 12: Project Structure

## Directory Structure

```
Practical 12/
│
├── 📁 backend/                    # Express.js API Server
│   ├── 📁 src/
│   │   ├── 📁 controllers/
│   │   │   └── todo.controller.js    # Business logic for todos
│   │   ├── 📁 models/
│   │   │   └── Todo.js               # Mongoose Todo model
│   │   ├── 📁 routes/
│   │   │   └── todo.routes.js        # API route definitions
│   │   └── server.js                 # Main Express server
│   ├── Dockerfile                    # Backend container config
│   ├── package.json                  # Backend dependencies
│   ├── .dockerignore                 # Files to exclude from Docker
│   └── .env.example                  # Environment variables template
│
├── 📁 frontend/                   # HTML/CSS/JS Frontend
│   ├── 📁 src/
│   │   ├── 📁 css/
│   │   │   └── style.css             # Application styles
│   │   ├── 📁 js/
│   │   │   └── app.js                # Frontend JavaScript logic
│   │   └── index.html                # Main HTML page
│   ├── Dockerfile                    # Frontend container config
│   ├── package.json                  # Frontend dependencies
│   └── .dockerignore                 # Files to exclude from Docker
│
├── docker-compose.yml              # Multi-container orchestration
├── README.md                       # Complete documentation
├── RUN_STEPS.md                   # Quick start guide
└── .gitignore                      # Git ignore rules
```

## Components Overview

### 🎨 Frontend (Port 3000)
- **Technology**: HTML5, CSS3, Vanilla JavaScript
- **Server**: live-server for development
- **Features**:
  - Add new todos
  - Toggle completion
  - Delete todos
  - Real-time statistics
  - Error handling
  - Loading states
  - Responsive design

### ⚙️ Backend (Port 5000)
- **Technology**: Node.js, Express.js
- **Database**: MongoDB with Mongoose
- **API Endpoints**:
  - `GET /api/todos` - Get all todos
  - `GET /api/todos/:id` - Get single todo
  - `POST /api/todos` - Create todo
  - `PUT /api/todos/:id` - Update todo
  - `PATCH /api/todos/:id/toggle` - Toggle completion
  - `DELETE /api/todos/:id` - Delete todo
  - `GET /api/health` - Health check

### 🗄️ Database (Port 27017)
- **Technology**: MongoDB 7.0
- **Features**:
  - Persistent storage via Docker volumes
  - Health checks
  - Automatic initialization

## Docker Services

### Service: mongo
- **Image**: mongo:7.0
- **Ports**: 27017:27017
- **Volumes**: mongo_data for persistence
- **Health Check**: Ensures database is ready

### Service: backend
- **Build**: ./backend/Dockerfile
- **Ports**: 5000:5000
- **Dependencies**: mongo (health check)
- **Environment**: MONGO_URI connection string

### Service: frontend
- **Build**: ./frontend/Dockerfile
- **Ports**: 3000:3000
- **Dependencies**: backend service

## Data Flow

```
User (Browser)
    ↓
Frontend (localhost:3000)
    ↓ HTTP Request
Backend API (localhost:5000)
    ↓ MongoDB Query
MongoDB (localhost:27017)
    ↓ Data Response
Backend → Frontend → User
```

## Docker Compose Network

All services communicate via `todo-network`:
- Frontend can reach Backend at `http://backend:5000`
- Backend can reach MongoDB at `mongodb://mongo:27017`

## Quick Start

1. **Start**: `docker-compose up`
2. **Access**: http://localhost:3000
3. **Stop**: `docker-compose down`
4. **Clean**: `docker-compose down -v`

## File Purposes

### Backend Files
- `server.js`: Express app setup, middleware, MongoDB connection
- `todo.controller.js`: CRUD operations logic
- `todo.routes.js`: API route definitions
- `Todo.js`: Mongoose schema and model
- `Dockerfile`: Container build instructions

### Frontend Files
- `index.html`: Main UI structure
- `style.css`: Responsive styling
- `app.js`: API calls, DOM manipulation, event handlers
- `Dockerfile`: Container build instructions

### Configuration Files
- `docker-compose.yml`: Multi-container orchestration
- `package.json`: Dependencies and scripts
- `.dockerignore`: Exclude files from Docker build
- `.env.example`: Environment variable template

## Key Features Demonstrated

✅ Docker containerization
✅ Docker Compose multi-container orchestration
✅ RESTful API design
✅ MongoDB integration
✅ Frontend-Backend communication
✅ CRUD operations
✅ Error handling
✅ Health checks
✅ Persistent data volumes
✅ Docker networking

## Next Steps

1. Review the code in each file
2. Run `docker-compose up` to start the application
3. Test all features (create, read, update, delete)
4. Check data persistence by refreshing the page
5. Explore the Docker containers: `docker-compose ps`
6. View logs: `docker-compose logs -f`
