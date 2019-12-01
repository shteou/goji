import sys

from goji.jobs import *

# Applies all queued jobs and transitions to processing/failed
# as required
def command_process(jobs):
  print("Checking for duplicate jobs")
  duplicates = duplicate_jobs()
  if bool(duplicates):
    print("Error, found the following duplicate jobs: ", duplicates)
    sys.exit(1)
  print("No duplicates found")

  print(f"Processing jobs: {jobs}")
  for job in jobs:
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