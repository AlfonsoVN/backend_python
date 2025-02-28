from flask import Flask, request, jsonify
from flask_cors import CORS
from groq import Groq
import os

app = Flask(__name__)
CORS(app)

# Configura tu API key
api_key = os.environ.get("GROQ_API_KEY")  # Asegúrate de que la API Key esté configurada

# Inicializa el cliente Groq
client = Groq(api_key=api_key)

@app.route('/api/chat', methods=['POST'])
def chat():
    # Obtén el mensaje del usuario desde el cuerpo de la solicitud
    user_message = request.json.get("message")
    
    if not user_message:
        return jsonify({"error": "No message provided"}), 400
    
    # Realiza la consulta a la API de Groq
    try:
        chat_completion = client.chat.completions.create(
            messages=[{
                "role": "user",
                "content": user_message
            }],
            model="llama-3.3-70b-versatile",  # Ajusta el modelo según lo que desees
        )
        
        # Extrae la respuesta del bot
        bot_reply = chat_completion.choices[0].message.content
        
        return jsonify({"response": bot_reply})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
