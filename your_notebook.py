#!/usr/bin/env python
# coding: utf-8

# In[36]:


import sys
sys.path.append('/Users/mayongzhi/Desktop/bioinformatic_project/genotyping_tool/PySanger')
import os
from pysanger import *
import matplotlib.pyplot as plt


# In[49]:


def visualize_sanger_sequences(file_path, template, highlight_positions):
    # Extract filename without extension for saving figures
    base_name = os.path.basename(file_path).split('.')[0]

    # Read ABI data
    abidata = abi_to_dict(filename=file_path)
    
    # Generate consensus sequences (if needed)
    f_seq, r_seq = generate_consensusseq(abidata)
    
    # Visualize the Sanger sequences
    fig = visualize(abidata, template = template, region = "aligned", highlight_positions = highlight_positions)
    plt.title(base_name)

    print(f_seq, r_seq)
    # Save the figure
    #fig.savefig(f"{base_name}.png")
    #plt.close(fig)  # Close the figure to free memory


# In[50]:


visualize_sanger_sequences("/Users/mayongzhi/Desktop/bioinformatic_project/genotyping_tool/F38_otof-Rprimer.ab1", "ATGCCGTGTCAGGCCGGCTA", [4,10,14])


# In[45]:


test1_file_path = '/Users/mayongzhi/Desktop/聽損lab/定序/otof/SD240416039__240416M13B'
test2_file_path = '/Users/mayongzhi/Desktop/聽損lab/定序/otof/64-8_17-1130328-1_2024-03-28'
template = 'ATGCCGTGTCAGGCCGGCTA'
highlight_positions = [4,10,14]


# In[46]:


def multiple_pysanger_plot(file_path, template, highlight_positions):
    for f in os.listdir(file_path):
        if f.endswith('.ab1'):
            complete_file_path = os.path.join(file_path,f)
            visualize_sanger_sequences(complete_file_path, template, highlight_positions)
    


# In[47]:


multiple_pysanger_plot(test1_file_path, template, highlight_positions)


# In[48]:


multiple_pysanger_plot(test2_file_path, template, highlight_positions)

