#!/bin/bash

echo "Enter a string: "
read string

reversed_string=$(echo "$string" | rev)

if [ "$string" = "$reversed_string" ]; then
    echo "'$string' is a palindrome"
else
    echo "'$string' is not a palindrome"
fi
