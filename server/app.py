from flask import Flask, render_template, jsonify, request
import cv2
import numpy as np
from utils.get_data_faces import get_data_storage, extract_features
from utils.compare_faces import compare_faces
from .neurolink_detection import 

app = Flask(__name__)

@app.route(f'/')
def index():
    return render_template('index.html')

@app.route(f'/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route(f'register')
def register():
    pass

@app.route(f'/login', methods=['POST'])
def login():
    file = request.files['image'].read()
    lastname = request.form.get('nom').lower()
    firstname = request.form.get('prenom').lower()
    npimg = np.frombuffer(file, np.uint8)
    img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

    stored_features = get_data_storage(firstname=firstname, lastname=lastname)
    if stored_features is None:
        authorized = False
        return jsonify({'authorized': authorized, 'result': 'Aucune image de référence trouvée.'})
    
    
    uploaded_features = extract_features(img, firstname=firstname, lastname=lastname)

    if uploaded_features is None:
        authorized = False
        return jsonify({'authorized': authorized,'result': 'Aucun visage détecté dans l’image envoyée.'})
    
    if compare_faces(uploaded_features, stored_features):
        result = "Correspondance trouvée !"
        authorized = True
    else:
        result = 'Aucune correspondance trouvée.'
        authorized = False

    return jsonify({'authorized': authorized, 'result': result})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005, debug=True)