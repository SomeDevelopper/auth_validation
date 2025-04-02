from flask import Flask, render_template, jsonify, request
import cv2
import numpy as np
from utils.logs import log_request_info

app = Flask(__name__)

@app.route(f'/')
def index():
    return render_template('index.html')

@app.route(f'/upload', methods=['POST'])
@log_request_info
def upload():
    file = request.files['image'].read()
    npimg = np.frombuffer(file, np.uint8)
    img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    if len(faces) > 0:
        result = "Correspondance trouvée !"
    else:
        result = 'Aucune correspondance trouvée.'

    return jsonify({'result': result})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005, debug=True)