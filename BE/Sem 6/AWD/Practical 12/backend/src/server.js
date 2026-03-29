import express from 'express';
import mongoose from 'mongoose';
import cors from 'cors';
import dotenv from 'dotenv';
import todoRoutes from './routes/todo.routes.js';

dotenv.config();

const app = express();
const PORT = process.env.PORT || 5000;
const MONGO_URI = process.env.MONGO_URI || 'mongodb://mongo:27017/todoapp';

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// MongoDB Connection
mongoose
   .connect(MONGO_URI)
   .then(() => {
      console.log('✅ Connected to MongoDB');
   })
   .catch((err) => {
      console.error('❌ MongoDB connection error:', err);
      process.exit(1);
   });

// Routes
app.use('/api/todos', todoRoutes);

// Health check
app.get('/api/health', (req, res) => {
   res.json({
      status: 'OK',
      mongodb: mongoose.connection.readyState === 1 ? 'connected' : 'disconnected',
      timestamp: new Date().toISOString(),
   });
});

// Start server
app.listen(PORT, () => {
   console.log(`🚀 Server running on http://localhost:${PORT}`);
});

export default app;
