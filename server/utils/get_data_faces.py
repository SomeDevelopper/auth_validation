from cassandra.cluster import Cluster
import numpy as np
import cv2
import os

cluster = Cluster(contact_points=["52.47.174.221"])

session_log = cluster.connect()
session_log.set_keyspace('surveillance')

def extract_features(img, firstname: str, lastname: str):
    """Détecte uniquement le visage principal et extrait ses caractéristiques"""
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.05, minNeighbors=7, minSize=(100, 100))

    if len(faces) == 0:
        print("Aucun visage détecté.")
        return None

    # On garde le plus grand visage
    faces = sorted(faces, key=lambda x: x[2] * x[3], reverse=True)  # Trier par aire (w*h)
    x, y, w, h = faces[0]
    
    print(f"Visage sélectionné à x={x}, y={y}, w={w}, h={h}")
    
    face_img = gray[y:y+h, x:x+w]

    image_name = f"./server/data_extracted/extracted_face_{firstname}_{lastname}.jpg"

    cv2.imwrite(image_name, face_img)
    print(f"Image du visage sauvegardée sous {image_name}")

    orb = cv2.ORB_create()
    keypoints, descriptors = orb.detectAndCompute(face_img, None)

    if descriptors is None:
        print("Impossible d’extraire des caractéristiques.")
    else:
        print(f"{len(descriptors)} caractéristiques extraites.")


    if descriptors is not None and len(descriptors) >= 50:
        print(f"Visage retenu avec {len(descriptors)} caractéristiques.")
        return descriptors
    else:
        print(f"Visage ignoré (trop peu de caractéristiques : {len(descriptors) if descriptors is not None else 0}).")
        return None
    


def get_data_storage(firstname: str, lastname: str):
    """Récupère l'image stockée et en extrait les caractéristiques"""
    # row = session_log.execute('SELECT image FROM wanted_infos').one()
    row = f'./server/data/{firstname}_{lastname}.jpg'
    if row:
        with open(row, 'rb') as img_f:
            npimg = np.frombuffer(img_f.read(), np.uint8)
            img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
            if img is None:
                print("Impossible de décoder l’image depuis la base de données.")
                return None
            if img is not None:
                return extract_features(img, firstname=firstname, lastname=lastname)
    return None