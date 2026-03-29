# Quick Run Steps - Practical 12

## Step 1: Navigate to Project Directory
```bash
cd "Practical 12"
```

## Step 2: Start Docker Containers
```bash
docker-compose up
```

## Step 3: Open Browser
Navigate to: **http://localhost:3000**

## Step 4: Test the Application
1. Add a new todo
2. Toggle completion
3. Delete todos
4. Refresh to check persistence

## Step 5: Stop Application
```bash
docker-compose down
```

## Troubleshooting

### If ports are already in use:
Check what's running on ports 3000, 5000, 27017:
```bash
lsof -i :3000
lsof -i :5000
lsof -i :27017
```

### View logs:
```bash
docker-compose logs -f
```

### Rebuild containers:
```bash
docker-compose down
docker-compose build
docker-compose up
```

### Clean everything (including database):
```bash
docker-compose down -v
docker-compose up
```
