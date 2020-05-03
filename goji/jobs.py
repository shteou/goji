import functools
import git
import os

from kubernetes import client, config
from kubernetes.utils import create_from_yaml

def job_states():
  return ["queued", "processing", "succeeded", "failed", "unknown"]

# Applies a job in the queued directory to kubernetes
# Returns whether or the job was applied successfuly
def apply_job(job_name):
  try:
    print("Applying job {job_name}")
    if os.environ["IN_CLUSTER"] == "true":
      k8s_config = config.load_incluster_config()
    else:
      k8s_config = config.load_kube_config()
    k8s_client = client.api_client.ApiClient(configuration=k8s_config)
    create_from_yaml(k8s_client, f"jobs/queued/{job_name}")
  except Exception as e:
    print(f"Failed to apply job {job_name}:")
    print(e)
    return False
  return True

# Move a job from one state to another, creating a commit and pushing the result
def move_job(filename, source_state, destination_state):
  print(f"Moving {filename} from {source_state} to {destination_state}")
  try:
    repo = git.Repo("jobs")
    repo.index.move([os.path.join(source_state, filename), os.path.join(destination_state, filename)])
    print(f"Committing state transition for {filename}")
    commit = repo.index.commit(f"{filename} transitioned from {source_state} to {destination_state}")
    print(f"Pushing commit {commit} for {filename}")
    origin = repo.remote(name='origin')
    origin.push()
  except Exception as e:
    print(f"Failed to move {filename}")
    print(e)
  print(f"Successfully moved {filename}")

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
