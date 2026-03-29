import { Router } from 'express';
import {
   getAllStudents,
   getStudentById,
   createStudent,
   updateStudent,
   deleteStudent,
} from '../controllers/studentController';

const router = Router();

// GET all students
router.get('/', getAllStudents);

// GET single student
router.get('/:id', getStudentById);

// POST create student
router.post('/', createStudent);

// PUT update student
router.put('/:id', updateStudent);

// DELETE student
router.delete('/:id', deleteStudent);

export default router;
