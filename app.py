import os
import base64
import logging
from flask import Flask, request, render_template, redirect, url_for
from sanger_analysis import visualize_sanger_sequence, multiple_pysanger_plot

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/single', methods=['GET', 'POST'])
def single():
    if request.method == 'POST':
        uploaded_file = request.files.get('file')
        if uploaded_file:
            template = request.form.get("template")
            highlight_positions = request.form.get("highlight_positions")

            # Ensure highlight_positions is a list of strings or integers
            highlight_positions = highlight_positions.split(',') if highlight_positions else []
            highlight_positions = [int(pos) for pos in highlight_positions if pos.isdigit()]

            img_buffer, f_seq, r_seq, file_name = visualize_sanger_sequence(uploaded_file, template, highlight_positions)
            img_base64 = base64.b64encode(img_buffer.getvalue()).decode('utf-8')

            result = {
                'image': img_base64,
                'f_seq': f_seq,
                'r_seq': r_seq,
                'filename' : file_name
            }
            
            return render_template('single_result.html', result=result)
    
    return render_template('single.html')

@app.route('/multiple', methods=['GET', 'POST'])
def multiple():
    if request.method == 'POST':
        uploaded_files = request.files.getlist('directory')
        template = request.form.get("template")
        
        # Ensure highlight_positions is a list of strings or integers
        highlight_positions = request.form.get("highlight_positions")
        highlight_positions = highlight_positions.split(',') if highlight_positions else []
        highlight_positions = [int(pos) for pos in highlight_positions if pos.isdigit()]

        if uploaded_files:
            files = [file for file in uploaded_files if file.filename.endswith('.ab1')]

            results = multiple_pysanger_plot(files, template, highlight_positions)
            
            for result in results:
                result['image'] = base64.b64encode(result['image'].getvalue()).decode('utf-8')
            
            return render_template('multiple_results.html', results=results)
    
    return render_template('multiple.html')


if __name__ == '__main__':
    app.run(debug=True)
