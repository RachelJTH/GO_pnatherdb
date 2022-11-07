#!/usr/bin/python
# -*- coding:utf-8 -*-

import requests, os, re
from inspect import currentframe, getframeinfo

'''
Ref:
http://pantherdb.org/services/openAPISpec.jsp
http://pantherdb.org/services/details.jsp

'''

####### customized region #######
inputfile = "C:/bigdata_project/1N219031407_1N922082201/20221024/1N219031407_1N922082201/2_GO enrichment/targeted_up_regulated_gene.txt"
organism_longname = "Caenorhabditis elegans"
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

go_enrich_api = "http://pantherdb.org/services/oai/pantherdb/enrich/overrep?"
taxon_id = get_taxon_id(main_url, organism_longname)
# ipt_list_str = get_gene_ipt_fmt(inputfile)
ipt_list_str = "Q96PB1"
# print(ipt_list_str)
labels = {'biological_process', 'molecular_function', 'cellular_component'}
test_type = 'FISHER' # FISHER(default) or BiNOMIAL
correct_type = 'FDR' # FDR(default), BONFERRONI, NONE
for data_type in labels:
    # param_obj = {'geneInputList':ipt_list_str, 'organism':taxon_id, 'refOrganism':taxon_id, 'annotDataSet':data_type, 'enrichmentTestType': test_type, 'correction': correct_type}
    go_enrich_api += "{0}{1}&{2}{3}&{4}{5}&{6}{7}&{8}{9}&{10}{11}".format("geneInputList=",ipt_list_str, 'organism=',taxon_id, 'refOrganism=',taxon_id, 'annotDataSet=', data_type,'enrichmentTestType=', test_type, 'correction=', correct_type) 
    res = requests.post(go_enrich_api)
    enrich_go_dict = res.json()
    print(enrich_go_dict['search'].keys())

#### TEST OUTPUT ####
# print(taxon_id)



# x = requests.post(url, json = myobj)

# print(x.text)