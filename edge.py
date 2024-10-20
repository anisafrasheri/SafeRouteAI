# You already have a Python API. You can extend its functionality as needed:

from flask import Flask, request, jsonify
import numpy as np

app = Flask(__name__)

@app.route('/check-safe-zone', methods=['POST'])
def check_safe_zone():
    data = request.json
    # Process location data and check against safe zones
    location = np.array(data['location'])
    is_safe = check_if_safe(location)  # Function to implement safety check
    return jsonify({"is_safe": is_safe})

def check_if_safe(location):
    # Logic to check if the area is safe or unsafe
    return True  # Or False based on conditions

if __name__ == '__main__':
    app.run(debug=True)
