// controllers/user.controller.ts
import { Request, Response } from 'express';

// Controller for user-related views
export const userController = {
  // Get all users view
  getAllUsers: (req: Request, res: Response) => {
    res.json({ message: 'Get all users' });
  },

  // Get single user view
  getUserById: (req: Request, res: Response) => {
    const { id } = req.params;
    res.json({ message: `Get user ${id}` });
  },

  // Create user view
  createUser: (req: Request, res: Response) => {
    const body = req.body;
    res.json({ message: 'Create user', data: body });
  },

  // Update user view
  updateUser: (req: Request, res: Response) => {
    const { id } = req.params;
    const body = req.body;
    res.json({ message: `Update user ${id}`, data: body });
  },

  // Delete user view
  deleteUser: (req: Request, res: Response) => {
    const { id } = req.params;
    res.json({ message: `Delete user ${id}` });
  }
};
