import Todo from '../models/Todo.js';

// Get all todos
export const getAllTodos = async (req, res) => {
   try {
      const todos = await Todo.find().sort({ createdAt: -1 });
      res.json({
         success: true,
         count: todos.length,
         data: todos,
      });
   } catch (error) {
      res.status(500).json({
         success: false,
         message: 'Error fetching todos',
         error: error.message,
      });
   }
};

// Get single todo
export const getTodoById = async (req, res) => {
   try {
      const todo = await Todo.findById(req.params.id);

      if (!todo) {
         return res.status(404).json({
            success: false,
            message: 'Todo not found',
         });
      }

      res.json({
         success: true,
         data: todo,
      });
   } catch (error) {
      res.status(500).json({
         success: false,
         message: 'Error fetching todo',
         error: error.message,
      });
   }
};

// Create new todo
export const createTodo = async (req, res) => {
   try {
      const { text } = req.body;

      if (!text) {
         return res.status(400).json({
            success: false,
            message: 'Todo text is required',
         });
      }

      const todo = await Todo.create({ text });

      res.status(201).json({
         success: true,
         message: 'Todo created successfully',
         data: todo,
      });
   } catch (error) {
      res.status(500).json({
         success: false,
         message: 'Error creating todo',
         error: error.message,
      });
   }
};

// Update todo
export const updateTodo = async (req, res) => {
   try {
      const { text, completed } = req.body;

      const todo = await Todo.findByIdAndUpdate(
         req.params.id,
         { text, completed },
         { new: true, runValidators: true }
      );

      if (!todo) {
         return res.status(404).json({
            success: false,
            message: 'Todo not found',
         });
      }

      res.json({
         success: true,
         message: 'Todo updated successfully',
         data: todo,
      });
   } catch (error) {
      res.status(500).json({
         success: false,
         message: 'Error updating todo',
         error: error.message,
      });
   }
};

// Delete todo
export const deleteTodo = async (req, res) => {
   try {
      const todo = await Todo.findByIdAndDelete(req.params.id);

      if (!todo) {
         return res.status(404).json({
            success: false,
            message: 'Todo not found',
         });
      }

      res.json({
         success: true,
         message: 'Todo deleted successfully',
         data: todo,
      });
   } catch (error) {
      res.status(500).json({
         success: false,
         message: 'Error deleting todo',
         error: error.message,
      });
   }
};

// Toggle todo completion
export const toggleTodo = async (req, res) => {
   try {
      const todo = await Todo.findById(req.params.id);

      if (!todo) {
         return res.status(404).json({
            success: false,
            message: 'Todo not found',
         });
      }

      todo.completed = !todo.completed;
      await todo.save();

      res.json({
         success: true,
         message: 'Todo toggled successfully',
         data: todo,
      });
   } catch (error) {
      res.status(500).json({
         success: false,
         message: 'Error toggling todo',
         error: error.message,
      });
   }
};
