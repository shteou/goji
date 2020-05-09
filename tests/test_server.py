import unittest

from mock import patch
from goji.server import health, github_webhook
from goji.webhook_processor import WEBHOOK_SUCCESS, WEBHOOK_INVALID_SECRET

class ServerTestCase(unittest.TestCase):
  def test_health(self):
    result = health()

    assert result == "OK!"

  @patch('goji.server.process_github_webhook')
  def test_webhook_valid(self, process_github_webhook):
    process_github_webhook.return_value = WEBHOOK_SUCCESS

    response = github_webhook()
    
    process_github_webhook.assert_called()
    assert response == "OK"

  @patch('goji.server.process_github_webhook')
  def test_webhook_invalid(self, process_github_webhook):
    process_github_webhook.return_value = WEBHOOK_INVALID_SECRET

    (response, code) = github_webhook()
    
    process_github_webhook.assert_called()
    assert response == "Invalid webhook signature"
    assert code == 400