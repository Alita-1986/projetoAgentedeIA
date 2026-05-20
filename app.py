
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from character import get_response

from elevenlabs.client import ElevenLabs
from dotenv import load_dotenv
import os

# =========================
# CONFIG
# =========================

load_dotenv()

client = ElevenLabs(
    api_key=os.getenv("ELEVEN_API_KEY")
)

app = Flask(__name__, static_folder='static')
CORS(app)

conversation_history = []

# =========================
# ROTAS
# =========================

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')


@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message', '')

    if not user_message:
        return jsonify({'error': 'Mensagem vazia'}), 400

    # =========================
    # IA RESPONDE
    # =========================

    reply = get_response(user_message, conversation_history)

    # salvar histórico
    conversation_history.append({
        "role": "user",
        "content": user_message
    })

    conversation_history.append({
        "role": "assistant",
        "content": reply
    })

    # =========================
    # GERAR ÁUDIO (ELEVENLABS)
    # =========================

    try:

        audio_stream = client.text_to_speech.convert(
            voice_id="oArP4WehPe3qjqvCwHNo",
            model_id="eleven_multilingual_v2",
            text=reply
        )

        audio_path = os.path.join("static", "voice.mp3")

        with open(audio_path, "wb") as f:
            for chunk in audio_stream:
                f.write(chunk)

        audio_url = "/static/voice.mp3"

    except Exception as e:
        print("ERRO AO GERAR ÁUDIO:", e)
        audio_url = None

    # =========================
    # RESPOSTA
    # =========================

    return jsonify({
        "response": reply,
        "audio": audio_url
    })


@app.route('/reset', methods=['POST'])
def reset():
    conversation_history.clear()
    return jsonify({'status': 'ok'})


# =========================
# RUN
# =========================

if __name__ == '__main__':
    app.run(debug=True, port=5000)

