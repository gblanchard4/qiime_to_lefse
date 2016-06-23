[![DOI](https://zenodo.org/badge/22868/gblanchard4/qiime_to_lefse.svg)](https://zenodo.org/badge/latestdoi/22868/gblanchard4/qiime_to_lefse)


# qiime_to_lefse
Convert Qiime taxa tables and mapping files to a LEfSe formatted file

# Description
This script was created in order to convert the Qiime pipeline files to LEfSe format easily. The script takes a Qiime mapping file and a Qiime OTU abundance table, along with any number of categories and will output a LEfSe table.

Categories must be comma separated

The default behavior is to collapse the unassigned reads during scrubbing of the original taxa headers ("k__", "p__", "c__", "o__", "f__", "g__", "s__").
The `--clean` option will remove the "Other" classification and sum the abundances with any name-collision it encounters.

# Usage:
`python qiime_to_lefse.py -m mappingfile.txt -t otus_L3.txt -c category1,category2,category3 -o converted_lefse.txt --clean`
