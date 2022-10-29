#!/bin/bash

start=`date +%s.%N`

echo Ececuting From BASH Script

python cleanUp.py

echo Execution Complete

end=`date +%s.%N`

echo runtime
echo "$end - $start" | bc -l