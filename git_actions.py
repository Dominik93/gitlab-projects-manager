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
    local_changes = not _is_clear(project_status)
    project['current_branch'] = current_branch
    project['local_changes'] = local_changes
    return {"name": project['name'], "branch": current_branch, "local_changes": local_changes}


def create_branch(directory: str, branch: str, project: dict):
    project_directory = f"{directory}/{project['namespace']}/{project['name']}"
    _git(f"git -C {project_directory} checkout -b {branch}")


def push(directory: str, project: dict):
    project_directory = f"{directory}/{project['namespace']}/{project['name']}"
    current_branch = _git(f"git -C {project_directory} branch --show-current")
    _git(f"git -C {project_directory} push -u origin {current_branch}")


def commit(directory: str, message: str, project: dict):
    project_directory = f"{directory}/{project['namespace']}/{project['name']}"
    _git(f'git -C {project_directory} commit -m "{message}"')


def pull(directory: str, default_branch: str, project: dict):
    project_directory = f"{directory}/{project['namespace']}/{project['name']}"
    current_branch = _git(f"git -C {project_directory} branch --show-current")
    if current_branch == default_branch:
        project_status = _git(f"git -C {project_directory} status")
        if _is_clear(project_status):
            _git(f"git -C {project_directory} pull")
