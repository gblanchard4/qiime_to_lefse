#! /usr/bin/env python
import argparse
import os
import sys
def format_from_map(mapping_file, categories, outfile):
	category1, category2 = categories.split(',')
	sample_id_list = []
	category1_list = []
	category2_list = []
	with open(mapping_file, 'r' ) as map_handle:
		for line in map_handle:
			if line.startswith('#'):
				header_list = line.rstrip().split('\t') 
				category1_index = header_list.index(category1)
				category2_index = header_list.index(category2)
			else:
				line_list = line.split('\t')
				sample_id_list.append(line_list[0])
				category1_list.append(line_list[category1_index])
				category2_list.append(line_list[category2_index])

	# Read file, now write lines sampleid, cat1, cat2
	with open(outfile, 'w') as lefse:
		lefse.write("SampleID\t{}\n".format('\t'.join(sample_id_list)))
		lefse.write("{}\t{}\n".format(category1, '\t'.join(category1_list)))
		lefse.write("{}\t{}\n".format(category2, '\t'.join(category2_list)))

def append_otu_info(taxa_table, outfile):
	taxa_headers = ["k__", "p__", "c__", "o__", "f__", "g__", "s__"]
	with open(taxa_table, 'r') as otus, open(outfile, 'a') as lefse:
		for line in otus:
			if not line.startswith('Taxon'):
				taxa, abundance =  line.split('\t', 1)
				# Replace semicolons with pipes
				taxa  = taxa.replace(';','|')
				# Remove headers
				for header in taxa_headers:
					if header in taxa:
						taxa = taxa.replace(header, '')
				# Remove orphan pipe
				taxa = taxa.rstrip('|')

				lefse.write("{}\t{}".format(taxa, abundance))


def main():
	# Get command line arguments
	parser = argparse.ArgumentParser(description='Convert a qiime workflow to proper lefse format')

	# Input file
	parser.add_argument('-m','--map',dest='map', help='The mapping file', required=True)
	parser.add_argument('-t','--taxa', dest='taxa', help='The tab delimeted percent abundance file', required=True)
	parser.add_argument('-c','--categories', dest='categories', help='Two comma-seperated categories', required=True)
	parser.add_argument('-o','--out', dest='outpath', help='The outpt file', required=True)
	
	args = parser.parse_args()
	mapping_file = os.path.abspath(args.map)
	taxa_table = os.path.abspath(args.taxa)
	categories =  args.categories
	outfile = os.path.abspath(args.outpath)

	# Check categories for error
	if not len(categories.split(',')) == 2:
		print "Error: Check categories"
		sys.exit()


	format_from_map(mapping_file, categories, outfile)
	append_otu_info(taxa_table, outfile)





if __name__ == '__main__':
	main()