#!/usr/bin/env python3

import argparse
import os
import sys

from GojiApp.commands.init import init
from GojiApp.commands.process import process
from GojiApp.jobs import *
from GojiApp.dir_tools import *

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

    process(list_job_files("queued"))


  def requeue(self):
    pass


  def init(self):
    parser = argparse.ArgumentParser(
               description='''Initialise the jobs directory

  If no repository is provided, scaffolds a new jobs repository
''')

    parser.add_argument('--repository', help="Specifies an existing jobs repository to clone")
    args = parser.parse_args(self.main_args[2:])

    init(args.repository)