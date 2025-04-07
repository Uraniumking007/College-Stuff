#!/bin/bash

read -p "Enter N number: " n
for i in $(seq 1 $n);
do
    read -p "Enter number n[$i]: " number[$i]
done


for i in $(seq 1 $n);
do
    echo "number[$i]: ${number[$i]} "
done

for (( i=0; i<n-1; i++ )); do
  for (( j=0; j<n-i-1; j++ )); do
    if [ ${number[j]} -gt ${number[j+1]} ]; then
      temp=${number[j]}
      number[j]=${number[j+1]}
      number[j+1]=$temp
    fi
  done
done

echo "Array in sorted order :"
echo ${number[*]}
