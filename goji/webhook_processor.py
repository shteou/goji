import hashlib, hmac, git, os, sys, threading, queue

from goji.logger import log
from goji.commands import process
from goji.jobs import list_job_files

WEBHOOK_INVALID_SECRET = "Invalid webhook secret provided"
WEBHOOK_SUCCESS = "OK"

repository = os.environ['GIT_REPOSITORY']
q = queue.Queue()
threading.Thread(target=worker, daemon=True).start()

def validate_github_webhook_secret(payload):
  digest_maker = hmac.new(os.environ["GITHUB_WEBHOOK_SECRET"].encode("utf-8"), bytearray(request.data), hashlib.sha1)
  if not hmac.compare_digest(digest_maker.hexdigest(), request.headers.get('X-Hub-Signature').replace("sha1=", "")):
    log.error("Invalid X-Hub-Signature in Github webhook call")
    return False
  return True

def process_github_webhook(payload):
  if not validate_github_webhook_secret(payload):
    return WEBHOOK_INVALID_SECRET

  if ("before" in payload or "after" in payload):
    log.info("Received webhook, checking for new queued jobs")
    q.put("webhook event")
  else:
    log.info("Received webhook for unrecognised event")

  return WEBHOOK_SUCCESS

def worker():
  while True:
    item = q.get()
    if not q.empty():
      log.info("Skipping current webhook, more webhooks are pending")
    else:
      if os.path.exists('jobs'):
        log.info("Pulling latest changes")
        repo = git.Repo('jobs')
        repo.remotes.origin.pull()
      elif repository:
        log.info(f"Cloning jobs directory from {repository}")
        os.makedirs("jobs")
        log.info(f"Cloning {repository}")
        repo = git.Repo.clone_from(repository, "jobs")
        log.info("Done")
      else:
        log.error("GIT_REPOSITORY not defined, unable to clone jobs repo")
        sys.exit(-1)

      jobs = list_job_files("queued")
      process.command_process(jobs)

    q.task_done()
