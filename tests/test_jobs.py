import unittest

from mock import patch
from goji.jobs import apply_job 

class JobsTestCase(unittest.TestCase):
  @patch('goji.jobs.client.api_client.ApiClient')
  @patch('goji.jobs.create_from_yaml')
  @patch('goji.jobs.config')
  @patch.dict('goji.jobs.os.environ', {"IN_CLUSTER": "false"})
  def test_apply_job_loads_kubeconfig(self, config, create_from_yaml, api_client):
    config.load_kube_config.return_value = {}
    api_client.return_value = "client"

    result = apply_job("foo")

    config.load_kube_config.assert_called()
    config.load_incluster_config.assert_not_called()
    create_from_yaml.assert_called_with("client", "jobs/queued/foo")
    assert result == True
  
  @patch('goji.jobs.client.api_client.ApiClient')
  @patch('goji.jobs.create_from_yaml')
  @patch('goji.jobs.config')
  @patch.dict('goji.jobs.os.environ', {"IN_CLUSTER": "true"})
  def test_apply_job_loads_incluster_config(self, config, create_from_yaml, api_client):
    config.load_incluster_config.return_value = {}
    api_client.return_value = "client"

    result = apply_job("foo")

    config.load_kube_config.assert_not_called()
    config.load_incluster_config.assert_called()
    create_from_yaml.assert_called_with("client", "jobs/queued/foo")
    assert result == True

  @patch('goji.jobs.client.api_client.ApiClient')
  @patch('goji.jobs.create_from_yaml')
  @patch('goji.jobs.config')
  def test_apply_job_fails_after_exception(self, config, create_from_yaml, api_client):
    config.load_kube_config.return_value = {}
    api_client.return_value = "client"
    create_from_yaml.side_effect = Exception("error")

    result = apply_job("foo")

    config.load_kube_config.assert_called()
    create_from_yaml.assert_called_with("client", "jobs/queued/foo")
    assert result == False  