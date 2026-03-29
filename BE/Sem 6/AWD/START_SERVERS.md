# 🚀 Starting Practical 12 (Development Mode)

## Backend & Frontend Must Be Running

The 404 error means the backend API server isn't running. You need to start BOTH servers.

---

## 📋 Quick Start Instructions

### Step 1: Start Backend Server

Open a terminal and run:

```bash
cd backend
bun run dev
```

**Expected output:**
```
✅ Connected to MongoDB
🚀 Server running on http://localhost:3000
```

**Keep this terminal open!**

---

### Step 2: Start Frontend Server

Open a NEW terminal (keep backend running) and run:

```bash
cd frontend
bun run dev
```

**Expected output:**
```
  ➜  Local:   http://localhost:4200/
  ➜  Network: use --host to expose
```

**Keep this terminal open too!**

---

### Step 3: Open Application

Open your browser and go to:

```
http://localhost:4200/#/practical12
```

---

## ✅ Verify It's Working

### Check Backend Health
Open browser and visit:
```
http://localhost:3000/api/health
```

Should see:
```json
{
  "status": "OK",
  "mongodb": "connected",
  "timestamp": "2025-03-29T..."
}
```

### Check Student API
Visit:
```
http://localhost:3000/api/students
```

Should see:
```json
{
  "success": true,
  "data": []
}
```

---

## 🔧 Troubleshooting

### Backend fails to start?

**MongoDB not running?**
```bash
# Start MongoDB
brew services start mongodb-community
# OR
mongod --config /usr/local/etc/mongod.conf
# OR use Docker
docker run -d -p 27017:27017 --name mongodb mongo:7.0
```

**Port 3000 in use?**
```bash
# Check what's using port 3000
lsof -i :3000
# Kill the process
kill -9 <PID>
```

**Bun not installed?**
```bash
# Install Bun
curl -fsSL https://bun.sh/install | bash
```

### Frontend fails to start?

**Port 4200 in use?**
```bash
lsof -i :4200
kill -9 <PID>
```

---

## 📝 Terminal Layout

You should have **2 terminals open**:

**Terminal 1 (Backend):**
```bash
cd backend
bun run dev
# Output: ✅ Connected to MongoDB
#         🚀 Server running on http://localhost:3000
```

**Terminal 2 (Frontend):**
```bash
cd frontend
bun run dev
# Output: ➜  Local:   http://localhost:4200/
```

---

## 🐳 Alternative: Docker Mode

If you want to avoid starting servers manually, use Docker:

```bash
docker-compose up --build
```

This starts everything automatically!
- MongoDB
- Backend (port 3000)
- Frontend (port 4200)

Then visit: http://localhost:4200/#/practical12

---

## 🎯 What Should Happen

Once both servers are running:

1. ✅ Browser shows Practical 12 page
2. ✅ Docker status shows:
   - Backend: "Running"
   - MongoDB: "Connected"
3. ✅ No 404 errors in console
4. ✅ Can add/edit/delete students
5. ✅ Data persists

---

## 📊 Server Status Check

**Backend is running if:**
- ✅ Terminal 1 shows "Server running on http://localhost:3000"
- ✅ http://localhost:3000/api/health returns JSON

**Frontend is running if:**
- ✅ Terminal 2 shows "Local: http://localhost:4200/"
- ✅ http://localhost:4200 loads the homepage

---

## 🚨 Still Getting 404?

1. **Check backend is running:**
   ```bash
   curl http://localhost:3000/api/health
   ```
   
2. **Check frontend can reach backend:**
   - Open browser DevTools (F12)
   - Go to Network tab
   - Look for failed requests to `/api/students`
   
3. **Check CORS is enabled:**
   - Backend should have: `app.use(cors())`
   - ✅ Already configured in server.ts

4. **Check proxy configuration:**
   - Frontend vite.config.js should proxy `/api` to backend
   - ✅ Already configured

---

**Start both servers now and the 404 error will disappear!** 🚀
