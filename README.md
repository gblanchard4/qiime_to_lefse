# qiime_to_lefse
Convert Qiime taxa tables and mapping files to a lefse formatted file

# Description
This script was created in order to convert the qiime pipeline files to lefse format easily. The script takes a qiime mapping file and a otu abundance table to convert to a lefse formated file. 
# Usage:
`python qiime_to_lefse.py -m mappingfile.txt -t otus_L3.txt -c category1,category2 -o converted_lefse.txt`