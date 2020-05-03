import sys

from goji.jobs import *

# Applies all queued jobs and transitions to processing/failed
# as required
def command_process(jobs):
  print("Checking for duplicate jobs")
  duplicates = duplicate_jobs()
  if len(duplicates) > 0 :
    print("Removing duplicate jobs")
    delete_jobs("queued", duplicates, "Deleting duplicated jobs")

  unique_jobs = [j for j in jobs if j not in duplicates]
  print(f"Processing remaining jobs: {unique_jobs}")
  for job in unique_jobs:
    try:
      print(f"Processing {job}")
      if apply_job(job):
        move_job(job, "queued", "processing")
        print(f"Processing {job} succeeded")
      else:
        move_job(job, "queued", "failed")
        print(f"Processing {job} failed")

    except Exception as e:
      print(f"Encountered an unexpected exception whilst processing {job}")
      print(e)

  print("Finished processing jobs")
