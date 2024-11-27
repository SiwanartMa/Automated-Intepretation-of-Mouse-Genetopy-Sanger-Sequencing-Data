import logging
import os
import io
import sys
import zipfile
import tempfile
import shutil
from flask import send_file
sys.path.append('/Users/mayongzhi/Desktop/bioinformatic_project/genotyping_tool/PySanger')
from pysanger import *
import matplotlib.pyplot as plt
matplotlib.use('Agg')  # Use the 'Agg' backend, which doesn't require a GUI

def visualize_sanger_sequence(file, template, highlight_positions):
    # Get the file content and filename
    file_content = file.read()
    file_name = file.filename

    # Create a BytesIO object to hold the file content
    file_buffer = io.BytesIO(file_content)

    # Read ABI data
    abidata = abi_to_dict(filename=file_buffer)
    
    # Generate consensus sequences
    f_seq, r_seq = generate_consensusseq(abidata)
    
    # Visualize the Sanger sequence
    fig = visualize(abidata, template=template, region="aligned", highlight_positions=highlight_positions)
    plt.title(file_name)

    # Save the figure to a BytesIO object
    img_buffer = io.BytesIO()
    fig.savefig(img_buffer, format='png', bbox_inches='tight')
    img_buffer.seek(0)
    
    plt.close(fig)  # Close the figure to free memory
    
    return img_buffer, f_seq, r_seq, file_name

def multiple_pysanger_plot(files, template, highlight_positions):
    results = []
    for file in files:
        # Generate the Sanger sequence visualization
        img_buffer, f_seq, r_seq, file_name = visualize_sanger_sequence(file, template, highlight_positions)

        # Logging for debugging
        logging.debug(f"Generated image for {file_name}: {img_buffer.getvalue()[:50]}...")

        results.append({
            'filename': file_name,
            'image': img_buffer
        })
    
    return results


