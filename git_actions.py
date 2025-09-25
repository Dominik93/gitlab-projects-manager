import os
import datetime

from commons.logger import log, Level


@log(Level.DEBUG, start_message="Execute {args}", end_message="Command executed {result} in {duration}ms")
def _git(command):
    command_result = os.popen(command).read().rstrip()
    if "fatal" in command_result:
        raise Exception
    return command_result


def _is_clear(project_status):
    return not ("Changes to be committed" in project_status or
                "Changes not staged for commit:" in project_status or
                "Your branch is ahead of" in project_status)


def clone(directory: str, project: dict):
    project_directory = f"{directory}/{project['namespace']}/{project['name']}"
    if not os.path.isdir(project_directory):
        _git(f"git clone {project['ssh']} {project_directory}")
    return status(directory, project)


def status(directory: str, project: dict):
    project_directory = f"{directory}/{project['namespace']}/{project['name']}"
    current_branch = _git(f"git -C {project_directory} branch --show-current")
    project_status = _git(f"git -C {project_directory} status")
    project['status'] = f'{current_branch}({"pristine" if _is_clear(project_status) else "dirty" })'
    project['modified'] = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
    return project


def create_branch(directory: str, branch: str, project: dict):
    project_directory = f"{directory}/{project['namespace']}/{project['name']}"
    _git(f"git -C {project_directory} checkout -b {branch}")


def push(directory: str, project: dict):
    project_directory = f"{directory}/{project['namespace']}/{project['name']}"
    current_branch = _git(f"git -C {project_directory} branch --show-current")
    _git(f"git -C {project_directory} push -u origin {current_branch}")


def commit(directory: str, message: str, project: dict):
    project_directory = f"{directory}/{project['namespace']}/{project['name']}"
    _git(f'git -C {project_directory} add .')
    _git(f'git -C {project_directory} commit -m "{message}"')


def checkout(directory: str, branch: str, project: dict):
    project_directory = f"{directory}/{project['namespace']}/{project['name']}"
    _git(f'git -C {project_directory} checkout {branch}')


def rollback(directory: str, project: dict):
    project_directory = f"{directory}/{project['namespace']}/{project['name']}"
    _git(f'git -C {project_directory} reset --hard')


def pull(directory: str, default_branch: str, project: dict):
    project_directory = f"{directory}/{project['namespace']}/{project['name']}"
    current_branch = _git(f"git -C {project_directory} branch --show-current")
    if current_branch == default_branch:
        project_status = _git(f"git -C {project_directory} status")
        if _is_clear(project_status):
            _git(f"git -C {project_directory} pull")
