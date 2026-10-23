from flask import Flask, request
import requests, os

app = Flask(__name__)

PHONE_NUMBER_ID = "1391576127373338"
VERIFY_TOKEN = "josperfume123"
OWNER_NUMBER = "2348084831989"

SHOP = {
    "name": "Jos Perfume",
    "opening": "8:00 AM",
    "closing": "8:00 PM",
    "location": "Terminus Market Jos, Plateau State",
    "account_name": "Hallys Integrated",
    "account_number": "8034682646",
    "bank": "Opay"
}

@app.route('/webhook', methods=['GET'])
def verify():
    if request.args.get("hub.verify_token") == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return "Forbidden", 403

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    try:
        value = data['entry'][0]['changes'][0]['value']
        if 'messages' not in value:
            return "OK", 200
        msg = value['messages'][0]
        from_number = msg['from']
        name = value.get('contacts', [{}])[0].get('profile', {}).get('name', 'there')
        text = msg['text']['body'].lower()
        original = msg['text']['body']
        
        if any(w in text for w in ["hi", "hello", "hey"]):
            reply = f"Hello {name} 😊 Welcome to Jos Perfume! How can I help?"
        elif any(w in text for w in ["account", "pay", "bank"]):
            reply = f"Bank: {SHOP['bank']}\nName: {SHOP['account_name']}\nNumber: {SHOP['account_number']}\n\nSend screenshot after payment 🙏"
        elif any(w in text for w in ["order", "buy", "want"]):
            reply = f"Got it {name}! Order '{original}' received. Forwarded to Oga ✅"
        else:
            reply = f"Hello {name}, ask me about products, price, location, account number, or place order."
        
        send_message(from_number, reply)
    except Exception as e:
        print(e)
    return "OK", 200

def send_message(to, text):
    token = os.getenv("WHATSAPP_TOKEN")
    url = f"https://graph.facebook.com/v25.0/{PHONE_NUMBER_ID}/messages"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    data = {"messaging_product": "whatsapp", "to": to, "type": "text", "text": {"body": text}}
    requests.post(url, headers=headers, json=data)

@app.route('/')
def home():
    return "Jos Perfume Bot Live!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
