import gseapy as gp
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from gseapy import Biomart
from time import strftime


####### customized region #######
# inputfile = "C:/bigdata_project/miRNA_mRNA analysis/piTa/src/2022nov_dev/GO_pantherdb_opt_test/gene_exp_list.txt" ## ENSEMBL gene id
# inputfile = "C:/Users/rachelhuang/OneDrive - 華聯生物科技股份有限公司/桌面/Rachel_main/others/Services/target_prediction/師大 鄭劍廷/miRNA-mRNA/metadata/results/CIRL_Sham_UP_merged_data/CIRL_Sham_UP_20230303-30_GO.txt"

pwd = "C:/Users/rachelhuang/OneDrive - 華聯生物科技股份有限公司/桌面/Rachel_main/others/Services/target_prediction/師大 鄭劍廷/miRNA-mRNA/metadata/results/CIRL_Sham_all/"

inputfile = os.path.join(pwd, "CIRL_Sham_all_unique.txt")

optfile = pwd

# organism_longname = "Homo sapiens" 
# organism_longname = "Rattus norvegicus" 

### Biomart dataset types
# ensembl_data_set = 'hsapiens_gene_ensembl'
ensembl_data_set = 'rnorvegicus_gene_ensembl'

### enrichr organism types
# organism_type: { ‘Human’, ‘Mouse’, ‘Yeast’, ‘Fly’, ‘Fish’, ‘Worm’ }
organism_type = "Mouse"

gene_library_sets = ['GO_Biological_Process_2021','KEGG_2019_Mouse', 'GO_Cellular_Component_2021', 'GO_Molecular_Function_2021']
### query library types:
### mouse_lib_types = gp.get_library_name(organism=organism_type)


#################################

file_date = strftime("_%Y%m%d-%S")
optfile_new = os.path.join(optfile, "GO"+file_date)
os.mkdir(optfile_new)

'''Convert Gene Identifiers: from gene id to gene name'''
bm = Biomart()

## BIOMART 
## view validated marts
# marts = bm.get_marts()
## view validated dataset
# datasets = bm.get_datasets(mart='ENSEMBL_MART_ENSEMBL')
## view validated attributes
# attrs = bm.get_attributes(dataset='hsapiens_gene_ensembl')
## view validated filters
# filters = bm.get_filters(dataset='hsapiens_gene_ensembl')
## query results
# queries ={'ensembl_gene_id': ['ENSRNOG00000000041','ENSRNOG00000000158', 'ENSRNOG00000000168', 'ENSRNOG00000000479', 'ENSRNOG00000000487', 'ENSRNOG00000000521', 'ENSRNOG00000000648', 'ENSRNOG00000000805', 'ENSRNOG00000000906', 'ENSRNOG00000001030', 'ENSRNOG00000001159', 'ENSRNOG00000001189']} # need to be a dict object

gene_list = pd.read_csv(inputfile, header=None, sep="\t")
print(gene_list.head())
gene_list = (gene_list.iloc[:, 0]).squeeze().str.strip().to_list()
# print(queries)
queries = {'ensembl_gene_id': gene_list}
gene_df = bm.query(dataset=ensembl_data_set,
                   attributes=['ensembl_gene_id', 'external_gene_name', 'entrezgene_id', 'go_id'],
                   filters=queries)
# print(gene_df.loc[:,'external_gene_name'])

gene_list = set()
for i, row in gene_df.loc[:,["external_gene_name"]].iterrows():
    if row.isna().any(): continue
    gene_list.add(row["external_gene_name"])
print(gene_list)
gene_list = list(gene_list)

## TEST 
# gene_list = ['IGKV4-1', 'CD55', 'IGKC', 'PPFIBP1', 'ABHD4', 'PCSK6', 'PGD', 'ARHGDIB', 'ITGB2', 'CARD6']


# print(glist)
# organism_type: { ‘Human’, ‘Mouse’, ‘Yeast’, ‘Fly’, ‘Fish’, ‘Worm’ }


''' Select Library Types '''
# mouse_lib_types = gp.get_library_name(organism=organism_type)
# print(mouse_lib_types) ### print all libraries which are related to the organism 

# go_bio = gp.get_library(name='GO_Biological_Process_2021', organism=organism_type)
# go_cell = gp.get_library(name='GO_Cellular_Component_2021', organism=organism_type)
# go_mol = gp.get_library(name='GO_Molecular_Function_2021', organism=organism_type)
# KEGG_2019_Mouse = gp.get_library(name='KEGG_2019_Mouse', organism=organism_type)

enr = gp.enrichr(gene_list=gene_list, 
                 gene_sets=gene_library_sets,
                 organism=organism_type, # don't forget to set organism to the one you desired! e.g. Yeast
                 outdir=optfile_new, # don't write to disk
                )

print(enr.results.head(5))

