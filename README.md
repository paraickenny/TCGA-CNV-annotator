# TCGA-CNV-annotator
Takes CNV data from cBioportal output file and writes bed files with hg38 coordinates for plotting on circos plots

# takes input of hg38 bed file listing genes and coordinates - "coordinates.txt"
# takes input of "CNA_Genes.tsv" files from cBioportal
# sample CNA file from "CNA Genes" table here: http://www.cbioportal.org/study?id=ucec_tcga_pan_can_atlas_2018
# appends proportion of CNVs at each gene from CNA file to coordinates
# outputs bed file with all information
