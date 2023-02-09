
#Importation
import os
from flask import Flask, request, jsonify
from firebase_admin import credentials, firestore, initialize_app


#Initialisation de la base de données FireStore 
app = Flask(__name__)


#
cred = credentials.Certificate('./datascientism-a9e6b-firebase-adminsdk-u4cdk-0ab2633879.json')
default_app = initialize_app(cred)
bd = firestore.client()
collection1 = bd.collection('all')


#Méthode create
PORT = 5000
@app.route('/add', methods=['POST'])
def create():
    """
        create() : Add document to Firestore collection with request body
        Ensure you pass a custom ID as part of json body in post request
        e.g. json={'id': '1', 'title': 'Write a blog post'}
    """
    try:
    
        collection1.add(request.json)
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occured: {e}"
    


#Méthode lire
@app.route('/lists', methods=['GET'])
def reads():
    """
        read() : Fetches documents from Firestore collection as JSON
        todo : Return document that matches query ID
        all_todos : Return all documents
    """
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
    """
        read() : Fetches documents from Firestore collection as JSON
        todo : Return document that matches query ID
        all_todos : Return all documents
    """
    try:
        
            all_todos = [doc.to_dict() for doc in collection1.stream()];
            print(all_todos)
            return jsonify(all_todos), 200
    except Exception as e:
        return f"An Error Occured: {e}"
    
    
if __name__ == '__main__':
    app.run(threaded=True, host='0.0.0.0', port=PORT, debug=True)