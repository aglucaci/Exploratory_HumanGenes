#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 16 14:31:24 2019

@author: alexander lucaci

a simple tool which uses gene names (Human Proteome Project) to find number of articles associated with a gene (Bibliography)
REF: https://en.wikipedia.org/wiki/List_of_human_genes
"""
# =============================================================================
# imports
# =============================================================================
from bs4 import BeautifulSoup
import requests, csv

# =============================================================================
# Declares
# =============================================================================
filename = "HPM_gene_level_epxression_matrix_Kim_et_al_052914.csv"
gene_dict = {}
counter = 0
gene_id = ""
url_gene_id = "https://www.ncbi.nlm.nih.gov/gene/?term="
url_get_items = "https://www.ncbi.nlm.nih.gov/pubmed?LinkName=gene_pubmed&from_uid="

# =============================================================================
# Helper Functions
# =============================================================================
def scrape_pubmed(url, mode):
    r  = requests.get(url)
    data = r.text
    soup = BeautifulSoup(data, features="lxml")

    if mode == "get_items":
        for h3 in soup.find_all('h3'):
            if "Items:" in h3.text:
                return h3.text.split(" ")[-1]
            
    if mode == "gene_id":
        for tr in soup.find_all("tr"):
            if "Homo sapiens" in tr.text:
                #print(tr.text.split(",")[0].split(" ")[3].isdigit())
                #print(tr.text.split(",")[0].split(" ")[2])
                
                gene_id = ""
                
                for x in tr.text.split(",")[0].split(" ")[3]:
                    
                    if x.isdigit() == True:
                        #print(type(x))
                        gene_id += x
                    else:
                        break
                return gene_id
            
# =============================================================================
# Main program starts here
# =============================================================================
#Initialize the gene dict
with open(filename, "r") as f:
    while True:
        line = f.readline()
        if line == "": break
        gene_dict[line.split(",")[0]] = 0
f.close()

for key in gene_dict:
    gene_id = scrape_pubmed(url_gene_id + key, "gene_id") 
    gene_dict[key] = scrape_pubmed(url_get_items + str(gene_id), "get_items")
    #print(key, gene_id, gene_dict[key], type(gene_dict[key]))
    w = csv.writer(open("output.csv", "a+"))
    w.writerow([key, gene_id, gene_dict[key]])
  
    
#DEBUG
#key = "DISC1"
#gene_id = scrape_pubmed(url_gene_id + key, "gene_id") 
#the_dict = scrape_pubmed(url_get_items + str(gene_id), "get_items")
#print(key, gene_id, the_dict, type(the_dict))

       
# =============================================================================
# End of file
# =============================================================================

"""
EXAMPLE

TP53 = 7157

https://www.ncbi.nlm.nih.gov/pubmed?LinkName=gene_pubmed&from_uid=7157
https://www.ncbi.nlm.nih.gov/gene/7157


"""
