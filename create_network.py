#!/usr/bin/env python

import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx

# Load data
input_file1 = sys.argv[1]
#network_df = pd.read_csv("./data/filtered_9606.protein.links.v11.0.txt", sep=" ")
network_df = pd.read_csv(input_file1, sep=" ")

input_file2 = sys.argv[2]
#domain_df = pd.read_csv("./data/protein_w_domains.txt", sep="\t")
domain_df = pd.read_csv(input_file2, sep="\t")

# Initialize a graph network
network = nx.from_pandas_edgelist(network_df, source='protein1', target='protein2', edge_attr='combined_score')

# Get nodes' degree
n_deg = network.degree
n_deg = pd.DataFrame.from_dict(n_deg)
n_deg.rename(columns={0:'protein',1:'degree'}, inplace=True)
n_deg['protein'] = n_deg['protein'].str.split('9606.').str[1]

# Get number of domains per protein
n_dom = domain_df.join(domain_df.groupby(['Protein stable ID'])['Pfam ID'].count(),on='Protein stable ID',rsuffix=' count')[['Protein stable ID','Pfam ID count']] 
n_dom = n_dom.drop_duplicates()
n_dom.rename(columns={'Protein stable ID':'protein'}, inplace=True)


# Merge 
merged_df = pd.merge(n_deg, n_dom, on='protein', how='inner')
merged_df['dummy_degree'] = np.where(merged_df['degree']>=100, '>=100degree','<100degree')

# Plot
fig, axes = plt.subplots(1,2)

# all data
p1 = sns.boxplot(data=merged_df,y="Pfam ID count",x="dummy_degree",ax=axes[0])
p1.set(xlabel=None)
p1.set(title='all data')

# remove 2 outliers
p2 = sns.boxplot(data=merged_df[merged_df['Pfam ID count']<100],y="Pfam ID count",x="dummy_degree", ax=axes[1])
p2.set(xlabel=None)
p2.set(title='removed 2 top outliers')

# Save output file
fig.savefig(sys.argv[3])

## ANSWER: There seems to not be a difference in terms of number of domains when it comes to high-node degree vs low-node degree proteins
