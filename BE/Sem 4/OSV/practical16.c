#include <stdio.h>
#include <unistd.h>
#include <sys/types.h>

int main() {
    pid_t pid;
    pid = fork();
    
    if (pid < 0) {
        fprintf(stderr, "Fork failed\n");
        return 1;
    }
    else if (pid == 0) {
        printf("This is child process\n");
        printf("Child Process ID: %d\n", getpid());
        printf("Child's Parent Process ID: %d\n", getppid());
    }
    else {
        printf("This is parent process\n");
        printf("Parent Process ID: %d\n", getpid());
        printf("Parent's Child Process ID: %d\n", pid);
    }
    
    return 0;
}