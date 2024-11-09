import os
import scipy.io
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS  # Import CORS
from io import BytesIO

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Route for home page
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle file upload and send EEG data points
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part', 400
    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400

    # Read file data into memory
    file_data = file.read()

    # Process and retrieve EEG data points
    eeg_data_points = retrieve_data_points(file_data)

    return jsonify({'eeg_data_points': eeg_data_points})

# Function to retrieve last 100 data points from MAT file
def retrieve_data_points(file_data):
    # Load the .mat file from memory
    mat_data = scipy.io.loadmat(BytesIO(file_data))

    # Access the EEG data from 'Clean_data'
    eeg_data = mat_data['Clean_data']
    num_channels, time_points = eeg_data.shape

    # Set the number of channels to retrieve data for
    num_channels_to_plot = 5  # Adjust if needed

    # Extract the last 100 data points for each specified channel
    eeg_last_100_points = {}
    for i in range(num_channels_to_plot):
        eeg_last_100_points[f'Channel {i+1}'] = eeg_data[i, -10000:].tolist()

    return eeg_last_100_points

if __name__ == '__main__':
    app.run(debug=True)
