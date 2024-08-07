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

    try:
        # Dummy context for the purpose of example
        context = (
            "We store detailed records of customer transactions, including purchase history, "
            "billing information, and customer support interactions. Our database also includes "
            "information on inventory levels, supplier details, and product specifications. "
            "Clients frequently inquire about their recent transactions, current account status, "
            "order history, and specific product details. Additionally, clients might ask about "
            "available inventory, the status of their support tickets, or upcoming promotions."
        )
        # Use the model to process the query
        response = nlp(question=user_query, context=context)
        response_text = response['answer']

        return jsonify({'response': response_text})

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
