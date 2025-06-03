import os

from commons.logger import log, Level


@log(Level.DEBUG, start_message="Execute {args}", end_message="Command executed {result} in {duration}ms")
def _git(command):
    return os.popen(command).read().rstrip()


def _is_clear(project_status):
    return not ("Changes to be committed" in project_status or
                "Changes not staged for commit:" in project_status or
                "Your branch is ahead of" in project_status)


def clone(directory: str, project: dict):
    project_directory = f"{directory}/{project['namespace']}/{project['name']}"
    if not os.path.isdir(project_directory):
        _git(f"git clone {project['ssh']} {project_directory}")


def status(directory: str, project: dict):
    project_directory = f"{directory}/{project['namespace']}/{project['name']}"
    current_branch = _git(f"git -C {project_directory} branch --show-current")
    project_status = _git(f"git -C {project_directory} status")
    project['current_branch'] = current_branch
    project['local_changes'] = current_branch
    return {"name": project['name'], "branch": current_branch, "local_changes": not _is_clear(project_status)}


def create_branch(directory: str, branch: str, project: dict):
    project_directory = f"{directory}/{project['namespace']}/{project['name']}"
    _git(f"git -C {project_directory} checkout -b {branch}")


def push(directory: str, project: dict):
    project_directory = f"{directory}/{project['namespace']}/{project['name']}"
    _git(f"git -C {project_directory} push")


def pull(directory: str, default_branch: str, project: dict):
    project_directory = f"{directory}/{project['namespace']}/{project['name']}"
    current_branch = _git(f"git -C {project_directory} branch --show-current")
    if current_branch == default_branch:
        project_status = _git(f"git -C {project_directory} status")
        if _is_clear(project_status):
            _git(f"git -C {project_directory} pull")
