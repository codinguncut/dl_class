#!/bin/bash
for section in $(ls -1 dl_class/lectures/)
do
	qpdf --empty --pages $(ls -1 dl_class/lectures/${section}/*.pdf | tr '\n' ' ') -- "./${section}.pdf"
done
