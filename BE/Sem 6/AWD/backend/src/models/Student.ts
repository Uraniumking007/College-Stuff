import mongoose, { Schema, Document } from 'mongoose';

export interface IStudent extends Document {
   name: string;
   email: string;
   age: number;
   course: string;
   createdAt: Date;
   updatedAt: Date;
}

const StudentSchema: Schema = new Schema(
   {
      name: {
         type: String,
         required: [true, 'Name is required'],
         trim: true,
      },
      email: {
         type: String,
         required: [true, 'Email is required'],
         unique: true,
         trim: true,
         lowercase: true,
      },
      age: {
         type: Number,
         required: [true, 'Age is required'],
         min: [1, 'Age must be at least 1'],
         max: [120, 'Age must be less than 120'],
      },
      course: {
         type: String,
         required: [true, 'Course is required'],
         trim: true,
      },
   },
   {
      timestamps: true,
   }
);

export default mongoose.model<IStudent>('Student', StudentSchema);
