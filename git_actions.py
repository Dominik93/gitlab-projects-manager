import argparse
import os

from commons.configuration_reader import read_configuration
from commons.countable_processor import CountableProcessor, ExceptionStrategy
from commons.csv_writer import write
from commons.logger import log, Level
from commons.store import create_store, Storage
from project_filter import filter_projects


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
    return {"name": project['name'], "branch": current_branch, "changes": _is_clear(project_status)}


def create_branch(directory: str, branch: str, project: dict):
    project_directory = f"{directory}/{project['namespace']}/{project['name']}"
    _git(f"git -C {project_directory} checkout -b {branch}")


def push(directory: str, project: dict):
    project_directory = f"{directory}/{project['namespace']}/{project['name']}"
    _git(f"git -C {project_directory} push")


def pull(directory: str, project: dict):
    default_branch = config.get_value("git.default_branch")
    project_directory = f"{directory}/{project['namespace']}/{project['name']}"
    current_branch = _git(f"git -C {project_directory} branch --show-current")
    if current_branch == default_branch:
        project_status = _git(f"git -C {project_directory} status")
        if _is_clear(project_status):
            _git(f"git -C {project_directory} pull")


def command_line_parser():
    parser = argparse.ArgumentParser(description='Gitlab project manager - git')
    parser.add_argument("--action", choices=['clone', 'pull', 'push', 'create-branch', 'status'],
                        help='Action to perform', required=True)
    parser.add_argument("--project-name", help='Name of project')
    parser.add_argument("--branch", help='Name of branch to create')
    parser.add_argument("--status-file", help='For action status, specify output file name',
                        default="status-{timestamp}.csv")
    args = parser.parse_args()
    return args.action, args.project_name, args.branch, args.status_file


if __name__ == "__main__":
    action, project_name, branch, status_file = command_line_parser()
    config = read_configuration("config")
    excluded = config.get_value("project.excluded")
    included = config.get_value("project.included")
    config_directory = config.get_value("management.directory")
    projects = create_store(Storage.JSON).load(lambda: {}, config.get_value("project_id"))
    projects = filter_projects(projects, excluded, included)
    if project_name is not None:
        projects = list(filter(lambda x: x["name"] == project_name, projects))
    strategy = ExceptionStrategy.PASS
    if action == 'clone':
        CountableProcessor(lambda x: clone(config_directory, x), strategy=strategy).run(projects)
    if action == 'pull':
        CountableProcessor(lambda x: pull(config_directory, x), strategy=strategy).run(projects)
    if action == 'push':
        CountableProcessor(lambda x: pull(config_directory, x), strategy=strategy).run(projects)
    if action == 'create-branch':
        CountableProcessor(lambda x: create_branch(config_directory, branch, x), strategy=strategy).run(projects)
    if action == 'status':
        projects_statues = CountableProcessor(lambda x: status(config_directory, x), strategy=strategy).run(projects)
        write(status_file, projects_statues)
