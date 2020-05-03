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
      repo = git.Repo('jobs')
      repo.remotes.origin.pull()
    elif repository:
      os.makedirs("jobs")
      print("Cloning " + repository)
      repo = git.Repo.clone_from(repository, "jobs")
      print("Done")

    print("Fetching latest repository")
    jobs = list_job_files("queued")
    print("Processing jobs")
    process.command_process(jobs)
    print(jobs)


    q.task_done()

threading.Thread(target=worker, daemon=True).start()

@app.route('/webhooks/github', methods=["POST"])
def github_webhook():
  payload = request.get_json()

  print("Payload:")
  print(payload)

  # TODO: Check secret and target repository matches expected repository
  if "before" in payload or "after" in payload:
    # Trigger a process event
    q.put("Event")
    return 'Toot!'
  else:
    return 'OK!'
