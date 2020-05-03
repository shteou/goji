import os
import sys

from goji.logger import log

def templates(args):
    return {
        "basic-job": f'''
apiVersion: batch/v1
kind: Job
metadata:
  name: {args.job_name}
spec:
  template:
    spec:
      containers:
      - name: {args.job_name}
        image: {args.image}
      restartPolicy: Never
  backoffLimit: 1
'''
    }


# Applies all queued jobs and transitions to processing/failed
# as required
def command_template(args):
  try:
    if args.template in templates(args):
      print(templates(args)[args.template])
    else:
      with open(args.template, "r") as template_file:
        new_job = template_file.read().format(args=args)
        with open(os.path.join("jobs", "queued", args.filename), "w+") as job_file:
          job_file.write(new_job)
    log.info("Template created")

  except Exception as e:
    log.error("Template creation failed")
    log.error(e)
    log.error(e.args)
