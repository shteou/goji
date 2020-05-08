import logger, sys

from goji.logger import log
from goji.jobs import *

def removeDuplicates(jobs):
  log.info("Checking for duplicate jobs")
  duplicates = duplicate_jobs()

  if len(duplicates) > 0 :
    log.warn(f"Removing duplicate jobs: {duplicates}")
    delete_jobs("queued", duplicates, "Deleting duplicated jobs")

  return [j for j in jobs if j not in duplicates]


def apply_job(job):
  try:
    log.info(f"Applying queued job: {job}")
    
    log_level, new_state = (logger.INFO, "processing") if apply_job(job) else (logger.WARNING, "failed")
    log.log(log_level, f"Applied queued {job}, new state is {new_state}")
    move_job(job, "queued", new_state)

  except Exception as e:
    log.error(f"Encountered an unexpected exception whilst processing {job}")
    log.error(e)

# Applies all queued jobs and transitions to processing/failed
# as required
def command_process(jobs):
  unique_jobs = removeDuplicates(jobs)

  log.info(f"Applying remaining queued jobs: {unique_jobs}")
  for job in unique_jobs:
    apply_job(job)

  log.info("Finished applying queued jobs")
