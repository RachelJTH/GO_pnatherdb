# Import Biopython modules to interact with KEGG
from Bio import SeqIO
from Bio.KEGG import REST
from Bio.KEGG.KGML import KGML_parser
from Bio.KEGG.Gene import parse
from Bio.Graphics.KGML_vis import KGMLCanvas

# Standard library packages
import io
import os
import pandas as pd

# Show images inline
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# Main Ref: https://widdowquinn.github.io/2018-03-06-ibioic/02-sequence_databases/09-KEGG_programming.html  (The james Hutton Institue)


# A bit of code that will help us display the PDF output
def PDF(filename):
    return HTML('<iframe src=%s width=700 height=350></iframe>' % filename)

# Some code to return a Pandas dataframe, given tabular text
def to_df(result):
    return pd.read_table(io.StringIO(result), header=None)

# perform the query
result = REST.kegg_info("kegg").read()
print(result)

# Print information about the PATHWAY database
# result = REST.kegg_info("pathway").read()
# print(result)


### TEST ""
# gene_list = "C:/bigdata_project/miRNA_mRNA analysis/piTa/src/2022nov_dev/GO_pantherdb_opt_test/kegg_test_gene_list.txt"

# with open(gene_list, "r") as handle:
#     for record in handle:

#         # records = record.split(",")
#         print(f"handle {record}")

# result = REST.kegg_get("map00061", "image").read()
# # image = mpimg.imread(result)
# plt.imshow(result)
# plt.show()

# Image(result)



