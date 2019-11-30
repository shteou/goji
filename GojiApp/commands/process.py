import sys

from GojiApp.jobs import *

# Applies all queued jobs and transitions to processing/failed
# as required
def process(jobs):
  duplicates = duplicate_jobs()
  if bool(duplicates):
    print("Error, found the following duplicate jobs: ", duplicates)
    sys.exit(1)

  for job in jobs:
    success = apply_job(job)
    if success == True:
      move_job(job, "queued", "processing")
    else:
      move_job(job, "queued", "failed")

