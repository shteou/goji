import unittest

from unittest import mock
from mock import patch

from goji.commands.process import command_process 

class CommandProcessTestCase(unittest.TestCase):
  @patch('goji.commands.process.duplicate_jobs')
  def test_command_proccess_empty_jobs(self, duplicate_jobs):
    duplicate_jobs.return_value = []

    command_process([])

    duplicate_jobs.assert_called()


  @patch('goji.commands.process.move_job')
  @patch('goji.commands.process.duplicate_jobs')
  @patch('goji.commands.process.delete_jobs')
  @patch('goji.commands.process.apply_job')
  def test_command_proccess_duplicate_jobs(self, apply_job, delete_jobs, duplicate_jobs, move_job):
    duplicate_jobs.return_value = ["foo"]

    command_process(["foo"])

    delete_jobs.assert_called_with("queued", ["foo"], "Deleting duplicated jobs")
    apply_job.assert_not_called()
    duplicate_jobs.assert_called()
    move_job.assert_not_called()

  @patch('goji.commands.process.move_job')
  @patch('goji.commands.process.duplicate_jobs')
  @patch('goji.commands.process.apply_job')
  def test_command_process_successful_job(self, apply_job, duplicate_jobs, move_job):
    duplicate_jobs.return_value = []
    apply_job.return_value = True

    command_process(["foo"])

    apply_job.assert_called_with("foo")
    duplicate_jobs.assert_called()
    move_job.assert_called_with("foo", "queued", "processing")


  @patch('goji.commands.process.move_job')
  @patch('goji.commands.process.duplicate_jobs')
  @patch('goji.commands.process.apply_job')
  def test_command_process_failed_job(self, apply_job, duplicate_jobs, move_job):
    duplicate_jobs.return_value = []
    apply_job.return_value = False

    command_process(["foo"])

    apply_job.assert_called_with("foo")
    duplicate_jobs.assert_called()
    move_job.assert_called_with("foo", "queued", "failed")

