"""Clean-up script which removes cleanup workflow's previous runs.

Delete previous workflow runs of cleanup.yml.
"""

import os
from pathlib import Path

from github import Github


GITHUB_REPOSITORY = os.environ["GITHUB_REPOSITORY"]
GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]
WORKFLOW_FILE = "cleanup.yml"


ROOT_DIR = Path(__file__).parents[3]
# check that workflow has been renamed or removed
if not (ROOT_DIR / ".github" / "workflows" / WORKFLOW_FILE).exists():
    raise FileNotFoundError("Workflow file does not exist!")


def main():
    repository = Github(GITHUB_TOKEN).get_repo(GITHUB_REPOSITORY)
    cleanup_workflow = repository.get_workflow(WORKFLOW_FILE)
    for run in cleanup_workflow.get_runs():
        run.delete()


if __name__ == "__main__":
    main()
