import express from 'express';
import {
   getAllTodos,
   getTodoById,
   createTodo,
   updateTodo,
   deleteTodo,
   toggleTodo,
} from '../controllers/todo.controller.js';

const router = express.Router();

router.route('/').get(getAllTodos).post(createTodo);
router.route('/:id').get(getTodoById).put(updateTodo).delete(deleteTodo);
router.patch('/:id/toggle', toggleTodo);

export default router;
