# takes input of hg38 bed file listing genes and coordinates - "coordinates.txt"
# takes input of "CNA_Genes.tsv" files from cBioportal
# sample CNA file from "CNA Genes" table here: http://www.cbioportal.org/study?id=ucec_tcga_pan_can_atlas_2018
# appends proportion of CNVs at each gene from CNA file to coordinates
# outputs bed file with all information

filename1 = "coordinates.txt"   # this coordinates file is in hg38
filename2 = "CNA_Genes.tsv"     # from cbioportal

genome = []
CNA_list = []

with open(filename2) as fh:             # imports the list of CNVs of genes from cBioportal
    while True:
        line2 = fh.readline().rstrip()  # read the first line
        line2 = line2.upper()
        if not line2: break
        if "GISTIC" not in line2:       # skips first line of file
            gene, gistic, cytoband, CNA, numberofsamples, percentageofcases = line2.split("\t")  # splits  line by tabs
            CNA_data = gene, gistic, cytoband, CNA, numberofsamples, percentageofcases   # makes a tuple of parameters
            CNA_data = list(CNA_data)   # converts tuple to a list
            CNA_list.append(CNA_data)   # adds list to overall list of CNAs

with open(filename1) as fh:
    while True:
        line1 = fh.readline().rstrip()  # read the first line
        line1 = line1.upper()           # changes all text to upper case
        if not line1: break
        if "Chromosome" not in line1:   # skips first line of file
            chr, start, end, karyotype, gene = line1.split("\t")    # splits each line by tabs
            coordinates = chr, start, end, karyotype, gene      # makes a tuple of key parameters
            coordinates = list(coordinates)                     # converts tuple to a list
            genome.append(coordinates)          # appends coordinates from line to genome list

for element in genome:
    test_gene = element[4]          # test_gene is the gene from the genome list to match with potential CNAs

    for c in CNA_list:
        if c[5] == "<0.1%":     # arbitratrily replaces scores of "<0.1%" with a lower number to facilitate graphing
            c[5] = "0.005%"
        c[5] = c[5].replace("%", "")    # removes % sign to allow use of the number in downstream files
        if test_gene == c[0]:           # append appropriate genome list element with CNA details
            element.append(c[3])
            element.append(c[4])
            element.append(c[5])
            break

outfile = raw_input("enter root name of filename for output (will be appended with _AMPS.bed etc. : ")

ampfile = str(outfile) + "_AMPS_only.bed"   # constructs strings for names of three output files
delfile = str(outfile) + "_DELS_only.bed"
allfile = str(outfile) + "_ALL.bed"

f_amp = open(ampfile, "w")                  # opens output files
f_del = open(delfile, "w")
f_all = open(allfile, "w")

line = "chromosome" + "\t" + "start" + "\t" + "end" + "\t" + "karyotype" + "\t" + "Gene" + "\t" + "CNA" + "\t" + "Total_Cases" + "\t" + "Percent_Cases" + "\n"  # write header
f_amp.write(line)
f_del.write(line)
f_all.write(line)

genome = genome[1:]     # removes first element from genome list. This is the old header

for element in genome:
    if len(element) < 8:  # equalizes fields in tab-delimited output file for rows with missing data
        if len(element) == 7:
            element.append("0")
        if len(element) == 6:
            element.append("0")
            element.append("0")
        if len(element) == 5:
            element.append("0")
            element.append("0")
            element.append("0")

    if "DEL" in element[4:]:       # adds a negative sign to % of cases with CNA for deletion cases (for graphs)
        element[7] = str("-" + element[7])

    parsedlist = ""          # parsed list holds the data from the element prior to writing to the file

    for a in element:
        parsedlist += a + "\t"
    parsedlist = parsedlist.rstrip("\t")    # get rid of final tab
    parsedlist = parsedlist + "\n"          # adds new-line to end

    if "AMP" in element[4:]:               # write to amplifications file if AMP
        f_amp.write(parsedlist)
    if "DEL" in element[4:]:               # write to deletions file if DEL
        f_del.write(parsedlist)
    f_all.write(parsedlist)                 # write to ALL file
f_amp.close()
f_del.close()
f_all.close()
