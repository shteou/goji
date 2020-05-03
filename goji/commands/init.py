import os
import git

from goji.logger import log
from goji.dir_tools import make_empty_git_dir
from goji.jobs import job_states

def command_init(repository):
    if os.path.exists('jobs'):
      log.info("jobs directory already exists... skipping")
    elif repository:
      os.makedirs("jobs")
      log.info("Cloning " + repository)
      git.Repo.clone_from(repository, "jobs")
      log.info("Done")
    else:
      log.info("Scaffolding a jobs repository")
      for d in map(lambda x: os.path.join("jobs", x), job_states()):
        make_empty_git_dir(d)
      log.info('''Done, please run:
  $ cd jobs
  $ git init
  $ git add .
  $ git commit -m 'initial commit'
  $ git remote origin add your-bare-repository
  $ git push origin master''')
