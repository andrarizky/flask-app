from flask import Flask, request
import requests

app = Flask(__name__)

OPENAI_API_KEY = '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'

@app.route('/whatsapp', methods=['POST'])
def whatsapp_webhook():
    incoming_message = request.form.get('Body')
    sender_number = request.form.get('From')

    # Kirim pesan ke OpenAI API
    headers = {"Authorization": f"Bearer {OPENAI_API_KEY}"}
    data = {
        "model": "text-davinci-003",
        "prompt": incoming_message,
        "max_tokens": 150
    }
    response = requests.post("https://api.openai.com/v1/completions", headers=headers, json=data)

    gpt_response = response.json().get('choices')[0].get('text').strip()

    # Balas pesan melalui Twilio
    twilio_response = f"<Response><Message>{gpt_response}</Message></Response>"
    return twilio_response, 200, {'Content-Type': 'application/xml'}

if __name__ == '__main__':
    app.run(debug=True)
