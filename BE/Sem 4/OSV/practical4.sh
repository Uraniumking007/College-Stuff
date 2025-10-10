#!/bin/bash

echo "--------------"

echo "Enter the Number of which you want multiplication table of: "
read number
for i in $( seq 10 )
do
echo "$number * $i = $(($number * $i))"
done
