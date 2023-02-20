
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
from colorDetectorFonctions import preprocess, rgb_to_hex, analyze, get_image
from PIL import Image
from pytesseract import pytesseract



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
def process_images():
    key = 'images_url'
    if key not in request.json:
        return {"Status":"error","Message":f"Vous n'avez pas spécifié {key}"}
    urls = request.json[key]
    resultats = []
    priority = 1
    for url in urls:
        image = get_image(url)
        processed_image = preprocess(image)
        colors = analyze(processed_image)
        color_results = []
        for color in colors:
            hex_color = rgb_to_hex(color)
            rgbColor = color.tolist()
            color_results.append({
                "priority": priority,
                "hex": hex_color,
                "rgb": f"rgb({rgbColor[0]},{rgbColor[1]},{rgbColor[2]})"
            })
            priority += 1
        resultats.append({
            "url": url,
            "colors": color_results
        })
    return resultats



#Méthode extraction de texte d'une image
@app.route('/extract', methods=['POST'])
def extract_text_from_images():
    tesseractPath = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    imageUrl = 'images_url'
    if imageUrl not in request.json:
        return {"Status":"error","Message":f"Vous n'avez pas spécifié {imageUrl}"}
    urls = request.json[imageUrl]
    resultats = []
    for url in urls:
        pytesseract.tesseract_cmd = tesseractPath
        image = get_image(imageUrl)
        extractedText = pytesseract.image_to_string(image)
        resultats.append({
            "url": url,
            "extractedText": extractedText
        })
        
    return resultats



if __name__ == '__main__':
    app.run(threaded=True, host='0.0.0.0', port=PORT, debug=True)
