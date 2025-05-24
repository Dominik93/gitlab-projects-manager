import os

from commons.configuration_reader import read_configuration
from commons.countable_processor import CountableProcessor, ExceptionStrategy
from commons.csv_writer import write
from commons.logger import log, Level
from commons.store import create_store, Storage
from project_filter import filter_projects


@log(Level.INFO, start_message="Execute {args}", end_message="Command executed {result} in {duration}ms")
def _git(command):
    return os.popen(command).read().rstrip()


def _is_clear(status):
    return not ("Changes to be committed" in status or
                "Changes not staged for commit:" in status or
                "Your branch is ahead of" in status)


def _clone(config, project):
    directory = config['management']['directory']
    project_directory = f"{directory}/{project['namespace']}/{project['name']}"
    if not os.path.isdir(project_directory):
        _git(f"git clone {project['ssh']} {project_directory}")


def _status(config, project):
    directory = config['management']['directory']
    project_directory = f"{directory}/{project['namespace']}/{project['name']}"
    current_branch = _git(f"git -C {project_directory} branch --show-current")
    status = _git(f"git -C {project_directory} status")
    return {"name": project['name'], "branch": current_branch, "changes": _is_clear(status)}


def _pull(config, project):
    directory = config['management']['directory']
    default_branch = config['git']['default_branch']
    project_directory = f"{directory}/{project['namespace']}/{project['name']}"
    current_branch = _git(f"git -C {project_directory} branch --show-current")
    if current_branch == default_branch:
        status = _git(f"git -C {project_directory} status")
        if _is_clear(status):
            _git(f"git -C {project_directory} pull")


if __name__ == "__main__":
    configuration = read_configuration("config")
    project = configuration['project']
    excluded = project['excluded']
    included = project['included']
    projects = create_store(Storage.JSON).load({}, project['group_id'])
    projects = filter_projects(projects, excluded, included)
    CountableProcessor(lambda x: _clone(configuration, x), strategy=ExceptionStrategy.PASS).run(projects)
    CountableProcessor(lambda x: _pull(configuration, x), strategy=ExceptionStrategy.PASS).run(projects)
    status = CountableProcessor(lambda x: _status(configuration, x), strategy=ExceptionStrategy.PASS).run(projects)
    write("status-{timestamp}.csv", status)
