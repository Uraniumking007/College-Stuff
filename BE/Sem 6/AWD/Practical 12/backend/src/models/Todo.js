import mongoose from 'mongoose';

const todoSchema = new mongoose.Schema(
   {
      text: {
         type: String,
         required: [true, 'Todo text is required'],
         trim: true,
      },
      completed: {
         type: Boolean,
         default: false,
      },
      createdAt: {
         type: Date,
         default: Date.now,
      },
   },
   {
      timestamps: true,
   }
);

const Todo = mongoose.model('Todo', todoSchema);

export default Todo;
