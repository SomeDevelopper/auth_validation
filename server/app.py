from flask import Flask, render_template, jsonify, request
#import cv2, os
import numpy as np, os, sys
#from utils.get_data_faces import get_data_storage, extract_features
#from utils.compare_faces import compare_faces
from utils.MongodbHelper import MongodbHelper

def func(*args, **kwargs): return
get_data_storage = func
extract_features = func
compare_faces = func

app = Flask(__name__)
session = {'authenticated': True}  # simule l'authentification

@app.route(f'/')
def index():
    return render_template('index.html')

@app.route(f'/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route(f'/register')
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

@app.route('/logout')
def logout():
    # Simulate logout by clearing the session
    session['authenticated'] = False
    return jsonify({'message': 'Logged out successfully'}), 200

@app.route('/warehouse')
def warehouse_init():
    # Simple authentication check (replace with your actual logic)
    return render_template('warehouse.html')

@app.route('/warehouse/add_document', methods=['POST'])
def add_document():
    # Simple authentication check (replace with your actual logic)
    if not session.get('authenticated'):
        return jsonify({'error': 'Authentication required'}), 401

    content = request.json.get('content')
    if not content:
        return jsonify({'error': 'Content is required'}), 400

    mongodb_helper = MongodbHelper(
        uri="",
        db_name="test_db",
        collection_name="collection_test",
        text_field="content"
    )
    try:
        document_id = mongodb_helper.add_document({'content': content})
        return jsonify({'message': 'Document added successfully', 'id': document_id}), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    
@app.route('/warehouse/find_similar', methods=['POST'])
def find_similar():
    if not session.get('authenticated'):
        return jsonify({'error': 'Authentication required'}), 401

    if not request.is_json:
        return jsonify({'error': 'Request must be JSON'}), 400

    input_text = request.json.get('input_text')
    if not input_text:
        return jsonify({'error': 'input_text field is required'}), 400

    mongodb_helper = MongodbHelper(
        uri="",
        db_name="test_db",
        collection_name="collection_test",
        text_field="content"
    )
    try:
        results = mongodb_helper.find_similar(input_text, top_x=5)
        return jsonify({'results': results}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005, debug=True)