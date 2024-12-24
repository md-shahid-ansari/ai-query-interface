from flask import Flask, request, jsonify
from transformers import pipeline
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS

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

if __name__ == '__main__':
    app.run(debug=True)
