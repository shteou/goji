import logging, sys

from goji.logger import log
from goji.jobs import apply_job, delete_jobs, duplicate_jobs, move_job 

def remove_duplicates(jobs):
  log.info("Checking for duplicate jobs")
  duplicates = duplicate_jobs()

  if len(duplicates) > 0 :
    log.warning(f"Removing duplicate jobs: {duplicates}")
    delete_jobs("queued", duplicates, "Deleting duplicated jobs")

  return [j for j in jobs if j not in duplicates]


def process_job(job):
  try:
    log.info(f"Applying queued job: {job}")
    
    log_level, new_state = (logging.INFO, "processing") if apply_job(job) else (logging.WARNING, "failed")
    log.log(log_level, f"Applied queued {job}, new state is {new_state}")
    move_job(job, "queued", new_state)

  except Exception as e:
    log.error(f"Encountered an unexpected exception whilst processing {job}")
    log.error(e)

# Applies all queued jobs and transitions to processing/failed
# as required
def command_process(jobs):
  unique_jobs = remove_duplicates(jobs)

  log.info(f"Applying remaining queued jobs: {unique_jobs}")
  for job in unique_jobs:
    process_job(job)

  log.info("Finished applying queued jobs")
