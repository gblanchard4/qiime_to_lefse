#! /usr/bin/env python
import argparse
import os
import sys

def append_otu_info(taxa_table, outfile, sample_dict, categories):
	category1, category2 = categories.split(',')
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
				category1_line = "{}\t".format(category1)
				category2_line = "{}\t".format(category2)
				#Split the line and exclude the "Taxon"
				for sample_id in line.rstrip('\n').split('\t')[1::]:
					# Add cat1 value to buffer
					category1_line += "{}\t".format(sample_dict[sample_id][0])
					# Add cat2 value to buffer
					category2_line += "{}\t".format(sample_dict[sample_id][1])
				# Add newlines
				category1_line += "\n"
				category2_line += "\n"
				# Write Lines
				lefse.write(category1_line)
				lefse.write(category2_line)
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

def map_to_dictionary(mapping_file, categories):
	sample_dict = {}
	category1, category2 = categories.split(',')
	with open(mapping_file, 'r' ) as map_handle:
		for line in map_handle:
			if line.startswith('#'):
				header_list = line.rstrip().split('\t') 
				category1_index = header_list.index(category1)
				category2_index = header_list.index(category2)
			else:
				line_list = line.split('\t')
				sample_id = line_list[0]
				category1_value = line_list[category1_index]
				category2_value = line_list[category2_index]
				sample_dict[sample_id] = (category1_value, category2_value)
	return sample_dict







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

	sample_dict = map_to_dictionary(mapping_file, categories)
	append_otu_info(taxa_table, outfile, sample_dict, categories)





if __name__ == '__main__':
	main()