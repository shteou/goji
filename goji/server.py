import os, threading, queue

import git

from flask import Flask
from flask import request

from goji.commands import process
from goji.jobs import list_job_files


app = Flask(__name__)

@app.route('/health')
def health():
    return 'OK!'

q = queue.Queue()

def worker():
  while True:
    item = q.get()
    repository = os.environ['GIT_REPOSITORY']
    repo = None

    if os.path.exists('jobs'):
      print("Pulling latest changes")
      repo = git.Repo('jobs')
      repo.remotes.origin.pull()
    elif repository:
      print("Cloning jobs directory from {repository}")
      os.makedirs("jobs")
      print("Cloning " + repository)
      repo = git.Repo.clone_from(repository, "jobs")
      print("Done")

    jobs = list_job_files("queued")
    process.command_process(jobs)

    q.task_done()

threading.Thread(target=worker, daemon=True).start()

@app.route('/webhooks/github', methods=["POST"])
def github_webhook():
  payload = request.get_json()

  # TODO: Check secret and target repository matches expected repository
  if "before" in payload or "after" in payload:
    print("Received webhook, checking for new queued jobs")
    q.put("webhook event")
    return 'OK!'
  else:
    print("Received webhook, but not interested")
    return 'OK!'
