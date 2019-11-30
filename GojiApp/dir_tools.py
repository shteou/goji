import os

# Creates an empty directory with .gitkeep file for scaffolding
# a git repository file structure
def make_empty_git_dir(dir_name):
  os.makedirs(dir_name)
  f = open(os.path.join(dir_name, ".gitkeep"), "w+")
  f.close()
