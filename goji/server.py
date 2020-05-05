from goji.webhook_processor import process_github_webhook, WEBHOOK_INVALID_SECRET

from flask import Flask
from flask import request

app = Flask(__name__)

@app.route('/health')
def health():
    return 'OK!'

@app.route('/webhooks/github', methods=["POST"])
def github_webhook():
  response = process_github_webhook(request.get_json())

  if response == WEBHOOK_INVALID_SECRET:
    return response, 400
  return response

