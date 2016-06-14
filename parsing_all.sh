#!/bin/bash
SPATH=$(pwd)
while IFS='' read -r line || [[ -n "$line" ]]; do
    touch "./result/$line"
    echo "parsing $line"
    python parsing_all.py $line > "./result/$line"
done < "$1"

mkdir train val test
mv sw{2005-4000} ./train
mv sw{4003-4153} ./val
mv sw{4154-4484} ./test