from flask import Flask, request

app = Flask(__name__)

VERIFY_TOKEN = "josperfume123"

@app.route('/')
def home():
    return "Jos Perfume Bot Live - Ready for Facebook"

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        mode = request.args.get('hub.mode')
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')
        print(f"Verify attempt: mode={mode} token={token}")
        if mode == 'subscribe' and token == VERIFY_TOKEN:
            print("VERIFY SUCCESS")
            return challenge, 200
        else:
            print("VERIFY FAILED - token mismatch")
            return 'Forbidden', 403
    
    if request.method == 'POST':
        print("Received message:", request.json)
        return 'OK', 200

if __name__ == '__main__':
    app.run(port=5000)
