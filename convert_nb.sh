#!/bin/bash
for a in $(find -iname "*.ipynb")
do
	jupyter nbconvert --to pdf "$a"
done
