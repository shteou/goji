#!/usr/bin/env python3

import argparse
import functools
import os
import sys

from git import Repo

def job_states():
  return ["queued", "processing", "succeeded", "failed", "unknown"]

def move_job(file, state, next_state):
  pass

def apply_job(file):
  return True

# Move a job from one state to another, creating a commit and pushing the result
def move_job(filename, source_state, destination_state):
  print(f"Moving {filename} from {source_state} to {destination_state}")
  repo = Repo("jobs")
  repo.index.move([os.path.join(source_state, filename), os.path.join(destination_state, filename)])
  repo.index.commit(f"{filename} transitioned from {source_state} to {destination_state}")
  origin = repo.remote(name='origin')
  origin.push()

# Applies all queued jobs and transitions to processing/failed
# as required
def process_jobs(jobs):
  for job in jobs:
    success = apply_job(job)
    if success == True:
      move_job(job, "queued", "processing")
    else:
      move_job(job, "queued", "failed")

# Creates an empty directory with .gitkeep file for scaffolding
# a git repository file structure
def make_empty_git_dir(dir_name):
  os.makedirs(dir_name)
  f = open(os.path.join(dir_name, ".gitkeep"), "w+")
  f.close()

# Lists all jobs (i.e. yaml files) within a given state
def list_job_files(state):
  return list(filter(is_job_file, os.listdir(os.path.join("jobs", state))))


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


# Is a file a valid job file, i.e. has a yaml extension
def is_job_file(file):
  return file.endswith(".yaml")


class Goji(object):
  def __init__(self, main_args):
    self.main_args = main_args
    parser = argparse.ArgumentParser(
             description='Runs one off jobs on Kubernetes',
             usage='''goji <command> [<args>]

   process    Process gitops jobs
   requeue    Requeues a job which is in a failed or unknown state
   init       Scaffold a new jobs directory

''')

    parser.add_argument('command', help='Subcommand to run')
    args = parser.parse_args(self.main_args[1:2])

    if not hasattr(self, args.command):
            print(args.command + ' is not a valid command')
            parser.print_help()
            exit(1)

    getattr(self, args.command)()


  def process(self):
    parser = argparse.ArgumentParser(
               description='''Process all queued jobs and update state of running jobs

  Possible states:
    queued    - Will be run during the next process
    succeeded - The job succeeded
    failed    - The job failed and can be requeued
    unknown   - Job is missing and success/failure cannot be determined
''')
    parser.add_argument('--repository')
    args = parser.parse_args(self.main_args[2:])

    duplicates = duplicate_jobs()
    if bool(duplicates):
      print("Error, found the following duplicate jobs: ", duplicates)
      sys.exit(1)

    process_jobs(list_job_files("queued"))


  def requeue(self):
    pass


  def init(self):
    parser = argparse.ArgumentParser(
               description='''Initialise the jobs directory

  If no repository is provided, scaffolds a new jobs repository
''')

    parser.add_argument('--repository', help="Specifies an existing jobs repository to clone")
    args = parser.parse_args(self.main_args[2:])

    if os.path.exists('jobs'):
      print("jobs directory already exists... skipping")
    elif args.repository:
      os.makedirs("jobs")
      print("Cloning " + args.repository)
      Repo.clone_from(args.repository, "jobs")
      print("Done")
    else:
      print("Scaffolding a jobs repository")
      for d in map(lambda x: os.path.join("jobs", x), job_states()):
        make_empty_git_dir(d)
      print('''Done, please run:
  $ cd jobs
  $ git init
  $ git add .
  $ git commit -m 'initial commit'
  $ git remote origin add your-bare-repository
  $ git push origin master''')
