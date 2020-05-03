import hashlib, hmac, git, os, threading, queue

from flask import Flask
from flask import request

from goji.logger import log
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
      log.info("Pulling latest changes")
      repo = git.Repo('jobs')
      repo.remotes.origin.pull()
    elif repository:
      log.info("Cloning jobs directory from {repository}")
      os.makedirs("jobs")
      log.info("Cloning " + repository)
      repo = git.Repo.clone_from(repository, "jobs")
      log.info("Done")

    jobs = list_job_files("queued")
    process.command_process(jobs)

    q.task_done()

threading.Thread(target=worker, daemon=True).start()

@app.route('/webhooks/github', methods=["POST"])
def github_webhook():
  payload = request.get_json()

  # log.info(request.get_data())
  # log.info(type(request.get_data()))

  digest_maker = hmac.new(os.environ["GITHUB_WEBHOOK_SECRET"].encode("utf-8"), bytearray(request.data), hashlib.sha1)
  if not hmac.compare_digest(digest_maker.hexdigest(), request.headers.get('X-Hub-Signature').replace("sha1=", "")):
    log.error("Invalid X-Hub-Signature in Github webhook call")
    return "Not OK!"

  # TODO: Check target repository matches expected repository
  if ("before" in payload or "after" in payload):
    log.info("Received webhook, checking for new queued jobs")
    q.put("webhook event")
    return 'OK!'
  else:
    log.info("Received webhook, but not interested")
    return 'OK!'
