import os
import sys
sys.path.append('/Users/mayongzhi/Desktop/bioinformatic_project/genotyping_tool/PySanger')
from pysanger import *
import matplotlib
matplotlib.use('Agg')  # Use the 'Agg' backend, which doesn't require a GUI
import matplotlib.pyplot as plt
import io

def visualize_sanger_sequence(file_content, template, highlight_positions):
    # Create a BytesIO object to hold the file content
    file_buffer = io.BytesIO(file_content)
    
    # Read ABI data
    abidata = abi_to_dict(filename=file_buffer)
    
    # Generate consensus sequences
    f_seq, r_seq = generate_consensusseq(abidata)
    
    # Visualize the Sanger sequence
    fig = visualize(abidata, template=template, region="aligned", highlight_positions=highlight_positions)
    
    # Save the figure to a BytesIO object
    img_buffer = io.BytesIO()
    fig.savefig(img_buffer, format='png')
    img_buffer.seek(0)
    
    plt.close(fig)  # Close the figure to free memory
    
    return img_buffer, f_seq, r_seq

def multiple_pysanger_plot(files, template, highlight_positions):
    results = []
    for file in files:
        # Process file and generate plot
        fig = visualize_sanger_sequence(file, template, highlight_positions)
        
        # Save plot to BytesIO object
        img_buffer = io.BytesIO()
        fig.savefig(img_buffer, format='png')
        img_buffer.seek(0)
        
        results.append({
            'filename': file.filename,
            'image': img_buffer,
            # Add other result data as needed
        })
    return results