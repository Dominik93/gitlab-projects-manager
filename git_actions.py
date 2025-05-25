import os

from commons.configuration_reader import read_configuration, Config
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


def clone(config: Config, project):
    directory = config.get_value("management.directory")
    project_directory = f"{directory}/{project['namespace']}/{project['name']}"
    if not os.path.isdir(project_directory):
        _git(f"git clone {project['ssh']} {project_directory}")


def status(config: Config, project):
    directory = config.get_value("management.directory")
    project_directory = f"{directory}/{project['namespace']}/{project['name']}"
    current_branch = _git(f"git -C {project_directory} branch --show-current")
    project_status = _git(f"git -C {project_directory} status")
    return {"name": project['name'], "branch": current_branch, "changes": _is_clear(project_status)}


def create_branch(config: Config, branch, project):
    directory = config.get_value("management.directory")
    project_directory = f"{directory}/{project['namespace']}/{project['name']}"
    _git(f"git -C {project_directory} checkout -b {branch}")


def push(config: Config, project):
    directory = config.get_value("management.directory")
    project_directory = f"{directory}/{project['namespace']}/{project['name']}"
    _git(f"git -C {project_directory} push")


def pull(config: Config, project):
    directory = config.get_value("management.directory")
    default_branch = config.get_value("git.default_branch")
    project_directory = f"{directory}/{project['namespace']}/{project['name']}"
    current_branch = _git(f"git -C {project_directory} branch --show-current")
    if current_branch == default_branch:
        project_status = _git(f"git -C {project_directory} status")
        if _is_clear(project_status):
            _git(f"git -C {project_directory} pull")


if __name__ == "__main__":
    config = read_configuration("config")
    excluded = config.get_value("project.excluded")
    included = config.get_value("project.included")
    projects = create_store(Storage.JSON).load({}, config.get_value("project_id"))
    projects = filter_projects(projects, excluded, included)
    CountableProcessor(lambda x: clone(config, x), strategy=ExceptionStrategy.PASS).run(projects)
    CountableProcessor(lambda x: pull(config, x), strategy=ExceptionStrategy.PASS).run(projects)
    projects_statues = CountableProcessor(lambda x: status(config, x), strategy=ExceptionStrategy.PASS).run(projects)
    write("status-{timestamp}.csv", projects_statues)
