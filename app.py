from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Load environment variables
WHATSAPP_API_URL = "https://graph.facebook.com/v20.0/523844200821726/messages"
ACCESS_TOKEN = os.getenv("WHATSAPP_ACCESS_TOKEN")

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    if data:
        # Process incoming message
        print("Received:", data)
        
        # Example: Auto-reply to messages
        if "messages" in data.get("entry", [{}])[0].get("changes", [{}])[0].get("value", {}):
            sender_id = data["entry"][0]["changes"][0]["value"]["messages"][0]["from"]
            send_message(sender_id, "Thanks for your message! TipsterX is coming soon!")
    
    return jsonify({"status": "received"}), 200

def send_message(to, message):
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": message}
    }
    response = requests.post(WHATSAPP_API_URL, json=payload, headers=headers)
    print("Message sent:", response.json())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
