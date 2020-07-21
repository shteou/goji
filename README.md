# goji - test

![Python application](https://github.com/shteou/goji/workflows/Python%20application/badge.svg)

Goji is a tool which can be integrated into a CD pipeline (e.g. with Jenkins) to provide a
GitOps way of running one-off jobs.

Goji proccesses Kubernetes jobs in a git repository.  
Jobs are initially queued by committing a yaml file to the `queued` directory.  
When `goji process` is run, queued jobs are applied and moved to the `processing` directory.  
Goji will then check the state of any jobs in the `processing` directory:
  - if the job is still running, it remains in `processing`
  - if the job is failed, it is moved to `failed`
  - if the job is complete, it is moved to `succeeded`
  - if the job cannot be found, or is in some other unknown state, is is moved to `unknown`

Goji will commit any changes in state to the jobs repository and push these changes to the origin server

The separate jobs repository should be configured to execute `goji process` (and optionally goji

# Installation

`git clone git@github.com:shteou/goji.git`
`cd goji`
`virtualenv venv`
`source venv/bin/activate`
`pip install -r requirements.txt`
`./goji ...`

# Installation as a helm chart

The following values should be defined:

- GIT_USERNAME          - The github username
- GIT_PASSWORD          - The github password (or PAT)
- GIT_REPOSITORY        - The jobs repository
- GITHUB_WEBHOOK_SECRET - The secret configured in the webhook

By default, a cluster-wide role will be installed with access to create batch jobs.
This can be disabled by setting `defaultClusterRole` to false.
In this case, (cluster)roles should be bound to the `goji` service account.

# Usage

## Pre-requesities

Goji requires:

  - Python 3.x
  - A working git installation with read/write access to the target jobs repository
  - A working kubectl installation, set to the target context (and namespace, if jobs are not
    configured with an explicit namespace field)

`goji init --repository git@github.com:my-user/my-job-repo.git`
`goji process`

# Jobs format

Jobs are stored in a repository with the following structure:

```
jobs/
  failed/
  processing/
  queued/
    your-job.yaml
  succeeded/
    executed-job.yaml
  unknown/
```

Or, if the repository is cloned via the `goji init --repository` command, the top level path may be
removed, i.e.

```
failed/
process/
queued/
  your-job.yaml
succeed/
  executed-job.yaml
unknown/
```

New jobs should be committed to the queued folder on the master branch.  
Old jobs can be requeued via the `goji requeue <job_file>` command
