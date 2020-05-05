import sys

from goji.logger import log
from goji.jobs import *

def removeDuplicates(jobs):
  log.info("Checking for duplicate jobs")
  duplicates = duplicate_jobs()

  if len(duplicates) > 0 :
    log.warn(f"Removing duplicate jobs: {duplicates}")
    delete_jobs("queued", duplicates, "Deleting duplicated jobs")

  return [j for j in jobs if j not in duplicates]


def process_job(job):
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

# Applies all queued jobs and transitions to processing/failed
# as required
def command_process(jobs):
  unique_jobs = removeDuplicates(jobs)

  log.info(f"Processing remaining jobs: {unique_jobs}")
  for job in unique_jobs:
    process_job(job)

  log.info("Finished processing jobs")
