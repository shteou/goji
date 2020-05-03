import sys

from goji.logger import log
from goji.jobs import *

# Applies all queued jobs and transitions to processing/failed
# as required
def command_process(jobs):
  log.info("Checking for duplicate jobs")
  duplicates = duplicate_jobs()
  if len(duplicates) > 0 :
    log.warn("Removing duplicate jobs")
    delete_jobs("queued", duplicates, "Deleting duplicated jobs")

  unique_jobs = [j for j in jobs if j not in duplicates]
  log.info(f"Processing remaining jobs: {unique_jobs}")
  for job in unique_jobs:
    try:
      log.info(f"Processing {job}")
      if apply_job(job):
        move_job(job, "queued", "processing")
        log.info(f"Processing {job} succeeded")
      else:
        move_job(job, "queued", "failed")
        log.error(f"Processing {job} failed")

    except Exception as e:
      log.error(f"Encountered an unexpected exception whilst processing {job}")
      log.error(e)

  log.info("Finished processing jobs")
