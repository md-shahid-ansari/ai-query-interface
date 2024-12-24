from flask import Flask, request, jsonify
from transformers import pipeline
from flask_cors import CORS
from flask import send_from_directory
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

frontend = os.getenv('FRONTEND', 'http://localhost:3000')

app = Flask(__name__, static_url_path='', static_folder='./build', template_folder='./build')
CORS(app, resources={r"*": {"origins": frontend}})

# Load the NLP model
nlp = pipeline("question-answering")

@app.route('/query', methods=['POST'])
def query():
    data = request.get_json()
    user_query = data.get('query')
    context = data.get('context')

    try:
        # Use the model to process the query
        response = nlp(question=user_query, context=context)
        response_text = response['answer']

        return jsonify({'response': response_text})

    except Exception as e:
        return jsonify({'error': str(e)})
    

# Route to serve the React app's main index.html
@app.route('/')
@app.route('/<path:path>')
def serve_react(path=''):
    if path and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

# Additional route to serve static assets (CSS, JS, etc.)
@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory(os.path.join(app.static_folder, 'static'), path)


if __name__ == '__main__':
    app.run(debug=True)
