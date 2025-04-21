#!/bin/bash

# Create a sample file with city names if it doesn't exist
if [ ! -f City_names.txt ]; then
    cat > City_names.txt << EOF
Mumbai
Delhi
Bangalore
Hyderabad
Chennai
Kolkata
Ahmedabad
Pune
Jaipur
Surat
EOF
fi

# Main menu
while true; do
    echo "Main Menu"
    echo "Press 1 for using Grep Command"
    echo "Press 2 for using Egrep Command"
    echo "Press 3 for using Fgrep Command"
    echo "Press 4 to Exit"
    read -p "Enter your choice: " choice

    case $choice in
        1)
            echo "For single pattern search, Enter Pattern below:"
            read -p "> " pattern
            echo "Results:"
            grep "$pattern" City_names.txt
            ;;
        2)
            echo "For double Pattern search, Enter two patterns:"
            read -p "Pattern 1> " pattern1
            read -p "Pattern 2> " pattern2
            echo "Results for Pattern 1:"
            egrep "$pattern1" City_names.txt
            echo "Results for Pattern 2:"
            grep -E "$pattern2" City_names.txt
            ;;
        3)
            echo "For Pattern From a File, Enter Pattern:"
            read -p "> " pattern
            echo "Results:"
            fgrep "$pattern" City_names.txt
            ;;
        4)
            echo "Exiting..."
            exit 0
            ;;
        *)
            echo "Invalid option. Please try again."
            ;;
    esac
    echo -e "\n"
done