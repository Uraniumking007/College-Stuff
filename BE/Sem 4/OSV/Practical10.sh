#!/bin/bash

while true; do
    echo "1. Show Executable Files"
    echo "2. Show Directories"
    echo "3. Show Zero-sized Files"
    echo "4. Exit"
    read -p "Enter your choice (1-4): " choice

    case $choice in
        1)
            echo -e "\nExecutable Files:"
            find . -maxdepth 1 -type f -executable -exec ls -l {} \;
            read -p "Press Enter to continue..."
            ;;
        2)
            echo -e "\nDirectories:"
            find . -maxdepth 1 -type d -exec ls -ld {} \;
            read -p "Press Enter to continue..."
            ;;
        3)
            echo -e "\nZero-sized Files:"
            find . -maxdepth 1 -type f -size 0 -exec ls -l {} \;
            read -p "Press Enter to continue..."
            ;;
        4)
            echo "Exiting..."
            exit 0
            ;;
        *)
            echo "Invalid choice. Press Enter to continue..."
            read
            ;;
    esac
done