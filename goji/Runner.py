#!/usr/bin/env python3

import argparse
import os
import sys

from goji.commands.init import command_init
from goji.commands.process import command_process
from goji.commands.template import command_template
from goji.jobs import *
from goji.dir_tools import *

class Goji(object):
  def __init__(self, main_args):
    self.main_args = main_args
    parser = argparse.ArgumentParser(
             description="Runs one off jobs on Kubernetes",
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
    parser.add_argument("--repository")
    args = parser.parse_args(self.main_args[2:])

    command_process(list_job_files("queued"))


  def requeue(self):
    pass

  def template(self):
    parser = argparse.ArgumentParser(
               description='''Creates a new job from the supplied template and params

  Valid templates are:
    basic-job
''')

    parser.add_argument("template", help="Selects the desired built-in template or template file")
    parser.add_argument("job_name", help="Define the name of the job")
    parser.add_argument("image", help="Define the container image of the job" )
    parser.add_argument("filename", help="Define the output filename of the job" )
    args = parser.parse_args(self.main_args[2:])

    command_template(args)


  def init(self):
    parser = argparse.ArgumentParser(
               description='''Initialise the jobs directory

  If no repository is provided, scaffolds a new jobs repository
''')

    parser.add_argument("--repository", help="Specifies an existing jobs repository to clone")
    args = parser.parse_args(self.main_args[2:])

    command_init(args.repository)