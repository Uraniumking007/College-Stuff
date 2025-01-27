#!/bin/bash
echo "-----------------"

echo "Enter Student Name: "
read studentname
echo "Enter Subject 1 Marks:"
read sub1
echo "Enter Subject 2 Marks:"
read sub2
echo "Enter Subject 3 Marks:"
read sub3

echo $sub1

total=`expr $sub1  + $sub2 + $sub3`
echo "Total: $total"

percentage=`expr  $total / 3`

echo "Percentage: $percentage%"

if [ $percentage -ge 80 ]
then
echo "First Class with Distinction"
elif [ "$percentage" -ge 60 ]
then
echo "First Class"
elif [ "$percentage" -ge 40 ]
then
echo "Second Class"
else
echo "Fail"
fi
echo "------------------"
