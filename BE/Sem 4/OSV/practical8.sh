#!/bin/bash

echo "1) Display calender of current month"
echo "2) Display today's date and Time"
echo "3) Display usernames those are currently logged in the system"
echo "4) Display your name at given x, y position"
echo "5) Display your terminal number"
echo "6) Exit"

read -p "Enter Choice: " ch

case "$ch" in
1) echo "cal";;
2) date ;;
3) who;;
4) 
row = $(tput lines)
col = $(tput cols)
echo "Terminal window has $row rows and $col cols"
read -p "Enter X: " x
read -p "Enter Y: " y
read -p "Enter Name: " name

tput cup $x $y
echo "$name";;
5) tty;;
*) echo "Invalid Input";;
esac
