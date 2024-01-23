#!/bin/bash
# collate documents into weeks/ topics
mkdir collated_pdf
for section in $(ls -1 dl_class/lectures/)
do
	qpdf --empty --pages $(ls -1 dl_class/lectures/${section}/*.pdf | tr '\n' ' ') -- "collated_pdf/${section}.pdf"
done
