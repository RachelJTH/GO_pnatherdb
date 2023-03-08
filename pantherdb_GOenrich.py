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
inputfile = "C:/bigdata_project/miRNA_mRNA analysis/piTa/src/2022nov_dev/GO_pantherdb_opt_test/NIHMS1017634-supplement-Supplementary_Data_panthan_PosTEST.txt"
organism_longname = "Homo sapiens" 
# organism_longname = "Rattus norvegicus" 
optfile = "C:/bigdata_project/miRNA_mRNA analysis/piTa/src/2022nov_dev/GO_pantherdb_opt_test/NIHMS1017634_opt.txt"
#################################

####### Test Module #######
# inputfile = "C:/bigdata_project/1N219031407_1N922082201/20221024/1N219031407_1N922082201/2_GO enrichment/targeted_up_regulated_gene.txt"
# organism_longname = "Caenorhabditis elegans"
# optfile = "C:/bigdata_project/miRNA_mRNA analysis/piTa/src/GO_pnatherdb/opt_test.txt"
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

    # enrich_go_dict = res.json() ## transfer api return object to Dictionary object
    print(res)


    # print(enrich_go_dict['results']['result'])
    # pd_df = pd.Dat/aFrame(enrich_go_dict['results']['result'])

    ## filtering: query gene#
    # pd_df[(pd_df.number_in_list > 0) & (pd_df.number_in_list != "")]
    # filter_info = pd_df[pd_df.number_in_list > 0]
    # print(pd_df.number_in_list)
    # print(filter_info)
    # with open(optfile, 'w') as f:  
        # pd_df.to_csv(f, header=True, index=False, lineterminator="")
            
    # return go_enrich_api


## PANTHER Tool: Statistical Enrichment 

    '''## json.fmt - parameters:##
    {
    "results":{
        "number_in_list": 12,
        "fdr": 4.164200947441854E-4,
        "pValue": 5.271140439799815E-6,
        "mapped_id_list": {"mapped_id": [
                    "Q8N3A8",
                    ...
                    ]},
    }'''

def statistic_enrich(annot_data_set, ipt_exp_file):
    go_enrich_api = "http://pantherdb.org/services/oai/pantherdb/enrich/statenrich"
    correct_type = 'FDR' # FDR(default), BONFERRONI, NONE
    taxon_id = get_taxon_id(main_url, organism_longname)

    # go_enrich_api += "{0}{1}&{2}{3}&{4}{5}&{6}{7}{8}".format('organism=', taxon_id, 'annotDataSet=', annot_data_set, 'correction=', correct_type, "geneExp=@", ipt_exp_file, ";type=text/plain")
    file = {'geneExp': open(ipt_exp_file, 'rb')}
    values = {'organism': taxon_id, 'annotDataSet': annot_data_set, 'correction': correct_type}

    # print(f"cmd: {go_enrich_api}")
    res = requests.post(go_enrich_api, files=file, data=values)
    # enrich_go_dict = res.json() ## transfer api return object to Dictionary object
    print(res)


    ## workable cmd 
    ## 
    ## cmd = "curl -X POST \"http://pantherdb.org/services/oai/pantherdb/enrich/statenrich\" -H \"accept: application/json\" -H \"Content-Type: multipart/form-data\" -F \"organism=9606\" -F \"annotDataSet=GO:0008150\" -F \"correction=FDR\" -F \"geneExp=@C:/bigdata_project/miRNA_mRNA analysis/piTa/src/2022nov_dev/GO_pantherdb_opt_test/NIHMS1017634-100_test.txt;type=text/plain\""
    


# def set_conent(self, query_result):
#     query_result

def statistics_output_header(enrich_data):
    '''## json.fmt - parameters:##
    {
    "results":{
        "search": {
        "search_type": "statistical enrichment"
        },
        "tool_release_date": 20221017,
        "annotDataSet": "GO:0008150",
        "annot_version_release_date": "GO Ontology database DOI:  10.5281/zenodo.6799722 Released 2022-07-01",
        "correction": "FDR"
        }
    }

    ## json.fmt - input basic statistics:##
     {
    "results":{
        "input_list": {
        "organism": "Homo sapiens",
        "mapped_count": 18249,
        "mapped_id": ["A", "B", "C"]
        },
    }'''
    

#     enrich_data
#     logs = "".format()



# set_conent(query_result)

# def output(data):

# Analysis Type:	PANTHER Enrichment Test (release 20221017)
# Annotation Version and Release Date:	GO Ontology database DOI:  10.5281/zenodo.6799722 Released 2022-07-01
# Analyzed List:	test_GO.txt (Rattus norvegicus)
# Correction:	FDR
# GO biological process complete	number	overUnder	pvalue	fdr

# labels = {'biological_process':'GO:0008150', 'molecular_function':'GO:0003674', 'cellular_component':'GO:0005575'}
labels = {'biological_process':'GO:0008150'}
ipt_exp_file = "C:/bigdata_project/miRNA_mRNA analysis/piTa/src/2022nov_dev/GO_pantherdb_opt_test/NIHMS1017634-100_test.txt"
for label in labels:
    data_type = '%3A'.join(labels[label].split(":"))
    # overexpresentation(data_type) 
    statistic_enrich(data_type, ipt_exp_file)

#### TEST OUTPUT ####
# print(taxon_id)


