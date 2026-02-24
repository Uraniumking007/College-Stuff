# AngularJS + Node.js + MongoDB Workspace

A full-stack Bun workspace featuring AngularJS 1.8.2 frontend, Node.js backend with Express, and MongoDB database.

## 🏗️ Project Structure

```
.
├── package.json              # Root workspace configuration
├── docker-compose.yml        # MongoDB container setup
├── .gitignore
├── README.md
├── frontend/                 # AngularJS 1.8.2 application
│   ├── package.json
│   ├── vite.config.js       # Vite config with API proxy
│   ├── index.html           # Main HTML with AngularJS
│   └── src/
│       ├── app.js           # AngularJS app module & controller
│       └── views/
│           └── home.html    # Home view template
└── backend/                 # Node.js + Express + MongoDB API
    ├── package.json
    ├── tsconfig.json
    ├── .env                 # Environment variables
    ├── .env.example
    └── src/
        └── server.ts        # Express server with MongoDB
```

## 🚀 Quick Start

### Prerequisites

- [Bun](https://bun.sh/) >= 1.0.0
- [MongoDB](https://www.mongodb.com/) (local or MongoDB Atlas)
- Node.js >= 18.0.0

### Installation

1. **Install dependencies:**
   ```bash
   bun install
   ```

2. **Set up MongoDB:**

   **Option A: Docker (Recommended)**
   ```bash
   docker-compose up -d
   ```
   This starts MongoDB in a container on port 27017.

   **Option B: Local MongoDB**
   - Install MongoDB locally
   - Start MongoDB service: `mongod` or `brew services start mongodb-community`

   **Option C: MongoDB Atlas (Cloud)**
   - Create a free account at [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
   - Create a cluster and get your connection string
   - Update `backend/.env` with your connection string

3. **Configure environment:**
   ```bash
   # backend/.env is already configured for local MongoDB
   # For Atlas, update MONGO_URI with your connection string
   ```

### Development

Run both frontend and backend in development mode:

```bash
# Start both services
bun run dev

# Or run individually
bun run dev:frontend   # Frontend on http://localhost:4200
bun run dev:backend    # Backend on http://localhost:3000
```

### Production Build

```bash
bun run build
bun run start
```

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/items` | Get all items |
| GET | `/api/items/:id` | Get single item |
| POST | `/api/items` | Create new item |
| PUT | `/api/items/:id` | Update item |
| DELETE | `/api/items/:id` | Delete item |
| GET | `/api/health` | Health check |

## 🌐 Frontend Features

- **AngularJS 1.8.2** with ngRoute
- **Vite** for fast development and hot module replacement
- **Proxy** configuration to backend API
- **Responsive** design with modern CSS
- **CRUD** operations (Create, Read, Update, Delete)

## 🔧 Backend Features

- **Express.js** REST API
- **Mongoose** ODM for MongoDB
- **TypeScript** for type safety
- **CORS** enabled
- **Environment** configuration with dotenv

## 📦 Tech Stack

| Component | Technology |
|-----------|------------|
| **Runtime** | Bun |
| **Frontend** | AngularJS 1.8.2, Vite |
| **Backend** | Node.js, Express.js, TypeScript |
| **Database** | MongoDB with Mongoose |
| **Dev Tools** | Docker Compose (for MongoDB) |

## 🛠️ Available Scripts

| Command | Description |
|---------|-------------|
| `bun run dev` | Start both frontend and backend |
| `bun run dev:frontend` | Start frontend only |
| `bun run dev:backend` | Start backend only |
| `bun run build` | Build both for production |
| `bun run build:frontend` | Build frontend only |
| `bun run build:backend` | Build backend only |
| `bun run start` | Start production server |

## 📝 Environment Variables

Backend `.env` file:

```env
PORT=3000
MONGO_URI=mongodb://localhost:27017/angular-node-app
NODE_ENV=development
```

## 🐛 Troubleshooting

### MongoDB Connection Issues

If you see MongoDB connection errors:

1. **Local MongoDB:** Ensure MongoDB is running
   ```bash
   # Check if MongoDB is running
   ps aux | grep mongod

   # Start MongoDB
   brew services start mongodb-community  # macOS
   sudo systemctl start mongod           # Linux
   ```

2. **Atlas:** Verify your IP is whitelisted in Atlas security settings

### Frontend Not Connecting to Backend

1. Check if backend is running on port 3000
2. Verify the proxy configuration in `frontend/vite.config.js`
3. Check browser console for CORS errors

### Port Already in Use

Change ports in:
- Frontend: `frontend/vite.config.js` (server.port)
- Backend: `backend/.env` (PORT)

## 📄 License

MIT
