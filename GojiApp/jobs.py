import functools
import git
import os

def job_states():
  return ["queued", "processing", "succeeded", "failed", "unknown"]

def move_job(file, state, next_state):
  pass

def apply_job(file):
  return True

# Move a job from one state to another, creating a commit and pushing the result
def move_job(filename, source_state, destination_state):
  print(f"Moving {filename} from {source_state} to {destination_state}")
  repo = git.Repo("jobs")
  repo.index.move([os.path.join(source_state, filename), os.path.join(destination_state, filename)])
  repo.index.commit(f"{filename} transitioned from {source_state} to {destination_state}")
  origin = repo.remote(name='origin')
  origin.push()

# Lists all jobs (i.e. yaml files) within a given state
def list_job_files(state):
  return list(filter(is_job_file, os.listdir(os.path.join("jobs", state))))

# Is a file a valid job file, i.e. has a yaml extension
def is_job_file(file):
  return file.endswith(".yaml")

# Checks for any duplicate jobs
# A job is considered a duplicate if it is present in the queued
# directory and one other directory
def duplicate_jobs():
  search_states = filter(lambda x: x != "queued", job_states())
  existing_jobs = set(
    functools.reduce(lambda a,b: a.union(set(list_job_files(b))),
      search_states, set([])))

  queued_jobs = set(list_job_files("queued"))

  return existing_jobs.intersection(queued_jobs)
