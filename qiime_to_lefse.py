#!/usr/bin/env python
import argparse

__author__ = "Gene Blanchard"
__email__ = "me@geneblanchard.com"


def map_to_dictionary(mapping_file, categories):
    sample_dict = {}
    # Open the mapping file
    with open(mapping_file, 'r') as map_handle:
        for line in map_handle:
            # Look for the header line so we know where our desired values are
            if line.startswith('#SampleID'):
                header_list = line.rstrip().split('\t')
                # Build a list of desired values
                indicies = []
                for category in categories:
                    indicies.append(header_list.index(category))
            else:
                # Only retain the information about the categories we want
                line_list = line.rstrip().split('\t')
                sample_id = line_list[0]
                category_values = []
                for index in indicies:
                    category_values.append(line_list[index])
                sample_dict[sample_id] = category_values
    return sample_dict


def append_otu_info(taxa_table, outfile, sample_dict, categories):
    # Headers to strip off
    taxa_headers = ["k__", "p__", "c__", "o__", "f__", "g__", "s__"]
    # Open the files to read/wrire
    with open(taxa_table, 'r') as otus, open(outfile, 'w') as lefse:
        for line in otus:
            # Get the order of samples to write the category lines
            if line.startswith('Taxon'):
                # Write the sampleid line
                lefse.write(line)
                # Prepare the category lines
                for index, category in enumerate(categories):
                    category_line = "{}".format(category)
                    for sample_id in line.rstrip('\n').split('\t')[1::]:
                        category_line += "\t{}".format(sample_dict[sample_id][index])
                    category_line += "\n"
                    # Write the category line
                    lefse.write(category_line)
            if not line.startswith('Taxon'):
                taxa, abundance = line.split('\t', 1)
                # Replace semicolons with pipes
                taxa = taxa.replace(';', '|')
                # Remove headers
                for header in taxa_headers:
                    if header in taxa:
                        taxa = taxa.replace(header, '')
                # Remove orphan pipe
                taxa = taxa.rstrip('|')
                lefse.write("{}\t{}".format(taxa, abundance))


def main():
    # Argument Parser
    parser = argparse.ArgumentParser(description='Convert a qiime workflow to proper lefse format')

    # Mapping file
    parser.add_argument('-m', '--map', dest='map', help='The mapping file', required=True)
    # Taxa file
    parser.add_argument('-t', '--taxa', dest='taxa', help='The tab delimited percent abundance file', required=True)
    # Output file
    parser.add_argument('-o', '--output', dest='out', help='The Lefse formatted output file', required=True)
    # Categories
    parser.add_argument('-c', '--categories', dest='categories', nargs='*', help='Space seperated list of categories', required=True)

    # Parse arguments
    args = parser.parse_args()
    mapfile = args.map
    taxafile = args.taxa
    outfile = args.out
    categories = args.categories

    sample_dict = map_to_dictionary(mapfile, categories)
    append_otu_info(taxafile, outfile, sample_dict, categories)




if __name__ == '__main__':
    main()
