
#Importation
import os
from flask import Flask, request, jsonify
from firebase_admin import credentials, firestore, initialize_app
import cv2
import urllib.request
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
from sklearn.cluster import KMeans
import json




#Initialisation de la base de données FireStore 
app = Flask(__name__)





#Récupération de la clé pour l'authentification
cred = credentials.Certificate('./datascientism-a9e6b-firebase-adminsdk-u4cdk-0ab2633879.json')
default_app = initialize_app(cred)
bd = firestore.client()
collection1 = bd.collection('all')





#Méthode create
PORT = 5000
@app.route('/add', methods=['POST'])
def create():
    try:
    
        collection1.add(request.json)
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occured: {e}"
    




#Méthode lire tout
@app.route('/lists', methods=['GET'])
def reads():
    try:
        # Check if ID was passed to URL query
        todo_id = request.args.get('id')    
        if todo_id:
            todo = collection1.document(todo_id).get()
            return jsonify(todo.to_dict()), 200
        else:
            all_todos = [doc.to_dict() for doc in collection1.stream()]
            return jsonify(all_todos), 200
    except Exception as e:
        return f"An Error Occured: {e}"
    
 
 
 
 
    
#Méthode lire test
@app.route('/getAll', methods=['GET'])
def read():
    try:
        
            all_todos = [doc.to_dict() for doc in collection1.stream()];
            print(all_todos)
            return jsonify(all_todos), 200
    except Exception as e:
        return f"An Error Occured: {e}"



#Méthode détecteur de couleurs
@app.route('/detect', methods=['POST'])
def preprocess(raw):
    image = cv2.resize(raw, (900, 600), interpolation = cv2.INTER_AREA)                                          
    image = image.reshape(image.shape[0]*image.shape[1], 3)
    return image

def rgb_to_hex(rgb_color):
    hex_color = "#"
    for i in rgb_color:
        hex_color += ("{:02x}".format(int(i)))
    return hex_color

def analyze(img):
    clf = KMeans(n_clusters = 5)
    color_labels = clf.fit_predict(img)
    center_colors = clf.cluster_centers_
    counts = Counter(color_labels)
    ordered_colors = [center_colors[i] for i in counts.keys()]
    hex_colors = [rgb_to_hex(ordered_colors[i]) for i in counts.keys()]
    return hex_colors

def get_image(url):
    response = urllib.request.urlopen(url)
    image = np.asarray(bytearray(response.read()), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return image

def process_images(image_urls):
    resultats = []
    for url in image_urls:
        image = get_image(url)
        processed_image = preprocess(image)
        colors = analyze(processed_image)
        resultats.append({
            "url": url,
            "colors": colors
        })
    return resultats

def main(image_urls):
    resultats = process_images(image_urls)
    with open("results.json", "w") as f:
        f.write(json.dumps(resultats))


if __name__ == '__main__':
    app.run(threaded=True, host='0.0.0.0', port=PORT, debug=True)
    image_urls = [
        "https://exemple.com/image1.jpg",
        "https://exemple.com/image2.jpg",
    ]
    main(image_urls)
    