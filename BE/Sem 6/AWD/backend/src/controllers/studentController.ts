import { Request, Response } from 'express';
import Student from '../models/Student';

// Get all students
export const getAllStudents = async (req: Request, res: Response): Promise<void> => {
   try {
      const students = await Student.find().sort({ createdAt: -1 });
      res.json({
         success: true,
         data: students,
      });
   } catch (error) {
      res.status(500).json({
         success: false,
         message: 'Error fetching students',
         error: error instanceof Error ? error.message : 'Unknown error',
      });
   }
};

// Get single student by ID
export const getStudentById = async (req: Request, res: Response): Promise<void> => {
   try {
      const student = await Student.findById(req.params.id);

      if (!student) {
         res.status(404).json({
            success: false,
            message: 'Student not found',
         });
         return;
      }

      res.json({
         success: true,
         data: student,
      });
   } catch (error) {
      res.status(500).json({
         success: false,
         message: 'Error fetching student',
         error: error instanceof Error ? error.message : 'Unknown error',
      });
   }
};

// Create new student
export const createStudent = async (req: Request, res: Response): Promise<void> => {
   try {
      const student = await Student.create(req.body);

      res.status(201).json({
         success: true,
         message: 'Student created successfully',
         data: student,
      });
   } catch (error) {
      res.status(400).json({
         success: false,
         message: 'Error creating student',
         error: error instanceof Error ? error.message : 'Unknown error',
      });
   }
};

// Update student
export const updateStudent = async (req: Request, res: Response): Promise<void> => {
   try {
      const student = await Student.findByIdAndUpdate(
         req.params.id,
         req.body,
         { new: true, runValidators: true }
      );

      if (!student) {
         res.status(404).json({
            success: false,
            message: 'Student not found',
         });
         return;
      }

      res.json({
         success: true,
         message: 'Student updated successfully',
         data: student,
      });
   } catch (error) {
      res.status(400).json({
         success: false,
         message: 'Error updating student',
         error: error instanceof Error ? error.message : 'Unknown error',
      });
   }
};

// Delete student
export const deleteStudent = async (req: Request, res: Response): Promise<void> => {
   try {
      const student = await Student.findByIdAndDelete(req.params.id);

      if (!student) {
         res.status(404).json({
            success: false,
            message: 'Student not found',
         });
         return;
      }

      res.json({
         success: true,
         message: 'Student deleted successfully',
         data: student,
      });
   } catch (error) {
      res.status(500).json({
         success: false,
         message: 'Error deleting student',
         error: error instanceof Error ? error.message : 'Unknown error',
      });
   }
};
