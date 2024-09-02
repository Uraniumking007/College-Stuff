package com.example.practical12;

import android.os.Parcel;
import android.os.Parcelable;

import androidx.annotation.NonNull;

public class TaskRVModal implements Parcelable {
    private String taskId;
    private String taskName;
    private String taskDescription;
    private boolean isCompleted;

    public TaskRVModal() {

    }

    public TaskRVModal(String taskId, String taskName, String taskDescription, boolean isCompleted) {
        this.taskId = taskId;
        this.taskName = taskName;
        this.taskDescription = taskDescription;
        this.isCompleted = isCompleted;
    }

    protected TaskRVModal(Parcel in) {
        taskId = in.readString();
        taskName = in.readString();
        taskDescription = in.readString();
        isCompleted = in.readByte() != 0;
    }

    public static final Creator<TaskRVModal> CREATOR = new Creator<TaskRVModal>() {
        @Override
        public TaskRVModal createFromParcel(Parcel in) {
            return new TaskRVModal(in);
        }

        @Override
        public TaskRVModal[] newArray(int size) {
            return new TaskRVModal[size];
        }
    };

    public String getTaskId() {
        return taskId;
    }

    public void setTaskId(String taskId) {
        this.taskId = taskId;
    }

    public String getTaskName() {
        return taskName;
    }

    public void setTaskName(String taskName) {
        this.taskName = taskName;
    }

    public String getTaskDescription() {
        return taskDescription;
    }

    public void setTaskDescription(String taskDescription) {
        this.taskDescription = taskDescription;
    }

    public boolean isCompleted() {
        return isCompleted;
    }

    public void setCompleted(boolean completed) {
        isCompleted = completed;
    }

    @Override
    public int describeContents() {
        return 0;
    }

    @Override
    public void writeToParcel(@NonNull Parcel parcel, int i) {
        parcel.writeString(taskId);
        parcel.writeString(taskName);
        parcel.writeString(taskDescription);
        parcel.writeByte((byte) (isCompleted ? 1 : 0));
    }
}
