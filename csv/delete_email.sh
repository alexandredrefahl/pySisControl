#!/bin/bash
input="emails.txt"
while IFS= read -r line
do
   echo "$line"
#   for file in $(grep -l "$line"); do
#	awk '{print "rm "$1}' > doit.sh
#   done
done < "$input"


