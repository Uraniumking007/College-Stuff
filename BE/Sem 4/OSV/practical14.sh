#!/bin/bash

echo "Enter Valid Date"
read date
echo "You have entered $date"
date -d $date

if [ $? -eq 0 ]
then
    echo "Entered Date is Valid"
else
    echo "Entered Date is Invalid"
fi