#!/usr/bin/python
# -*- coding:utf-8 -*-

import requests, os, re
from inspect import currentframe, getframeinfo
import json
import pandas as pd
'''
Ref:
http://pantherdb.org/services/openAPISpec.jsp
http://pantherdb.org/services/details.jsp

'''

####### customized region #######
inputfile = "C:/bigdata_project/1N219031407_1N922082201/20221024/1N219031407_1N922082201/2_GO enrichment/targeted_up_regulated_gene.txt"
organism_longname = "Caenorhabditis elegans"
optfile = "C:/bigdata_project/miRNA_mRNA analysis/piTa/src/GO_pnatherdb/opt_test.txt"
#################################


main_url = 'http://pantherdb.org/'

## [API] Supported Genomes 
def get_taxon_id(main_url, organism_longname):
    supported_genome_api = "/services/oai/pantherdb/supportedgenomes"    
    res = requests.get("http://pantherdb.org/services/oai/pantherdb/supportedgenomes")
    status_code = res.status_code
    organism_dict = res.json()
    # print(type(status_code))
    # print(res.headers)
    # print(type(res.json()))
    # print(organism_dict.keys())
    # print(organism_dict['search'].keys())
    # print(organism_dict['search']['output']['genomes']['genome'])

    if status_code != 200:
        frameinfo = getframeinfo(currentframe())
        print('api request error: ', frameinfo.filename, frameinfo.lineno)
        return 
    else:
        organs = organism_dict['search']['output']['genomes']['genome']
        taxon_id = ""
        for organ in organs:
            # print(organ['long_name'], organism_longname)
            if organ['long_name'] == organism_longname:
                taxon_id = organ['taxon_id']
                return taxon_id
        return taxon_id

def get_gene_ipt_fmt(inputfile):
    inupt_set = set()   
    with open(inputfile, 'r') as f:
        for line in f:
            inupt_set.add(line.strip())
    ipt_list_str = ",".join(inupt_set)
    return ipt_list_str
 

## GO 
## PANTHER Tool: Enrichment (overrepresentation) 

def overexpresentation(data_type):
    go_enrich_api = "http://pantherdb.org/services/oai/pantherdb/enrich/overrep?"
    
    test_type = 'FISHER' # FISHER(default) or BiNOMIAL
    correct_type = 'FDR' # FDR(default), BONFERRONI, NONE
    taxon_id = get_taxon_id(main_url, organism_longname)
    ###### Test ######
    # ipt_list_str = "WBGene00010256,WBGene00016022"
    # taxon_id = 9606
    ##################
    ipt_list_str = get_gene_ipt_fmt(inputfile)
    
    # param_obj = {'geneInputList':ipt_list_str, 'organism':taxon_id, 'refOrganism':taxon_id, 'annotDataSet':data_type, 'enrichmentTestType': test_type, 'correction': correct_type}
    go_enrich_api += "{0}{1}&{2}{3}&{4}{5}&{6}{7}&{8}{9}&{10}{11}".format("geneInputList=",ipt_list_str, 'organism=',taxon_id, 'refOrganism=',taxon_id, 'annotDataSet=', data_type,'enrichmentTestType=', test_type, 'correction=', correct_type) 
    res = requests.post(go_enrich_api)
    enrich_go_dict = res.json() ## transfer api return object to Dictionary object

    # print(enrich_go_dict['results']['result'])
    pd_df = pd.DataFrame(enrich_go_dict['results']['result'])

    ## filtering: query gene#
    pd_df[(pd_df.number_in_list > 0) & (pd_df.number_in_list != "")]

    # print(pd_df.number_in_list)

    with open(optfile, 'w') as f:  
        pd_df.to_csv(f, header=True, index=False, sep="\t", lineterminator="")
            
    return go_enrich_api


# labels = {'biological_process':'GO:0008150', 'molecular_function':'GO:0003674', 'cellular_component':'GO:0005575'}
labels = {'biological_process':'GO:0008150'}
for label in labels:
    data_type = '%3A'.join(labels[label].split(":"))
    overexpresentation(data_type)   

#### TEST OUTPUT ####
# print(taxon_id)