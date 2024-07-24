from flask import Flask, render_template, request, send_file
from sanger_analysis import multiple_pysanger_plot
import io
import os

print("Current working directory:", os.getcwd())

# Add this line to print out the absolute path of the templates folder
print("Templates folder:", os.path.abspath(os.path.join(os.getcwd(), 'templates')))

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    print("Attempting to render index.html")
    if request.method == 'POST':
        files = request.files.getlist('files')
        print("POST request received")
        template = request.form['template']
        highlight_positions = [int(pos) for pos in request.form['highlight_positions'].split(',')]
        results = multiple_pysanger_plot(files, template, highlight_positions)
        app.config['RESULTS'] = results  # Store results in app config
        print(f"Number of results: {len(results)}")
        return render_template('results.html', results=results)
    print("Rendering index.html")
    return render_template('index.html')

@app.route('/image/<int:index>')
def get_image(index):
    results = app.config['RESULTS']
    img_buffer = results[index]['image']
    img_buffer.seek(0)
    return send_file(img_buffer, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)