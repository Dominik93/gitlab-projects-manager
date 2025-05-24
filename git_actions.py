import os

from commons.countable_processor import CountableProcessor, ExceptionStrategy
from commons.logger import log, Level
from commons.store import create_store, Storage
from configuration_reader import read_configuration


@log(Level.INFO, start_message="Execute {args}", end_message="Command {args} executed in {duration}ms")
def _git(command):
    return os.popen(command).read()


def _is_clear(status):
    return not ("Changes to be committed" in status or
                "Changes not staged for commit:" in status or
                "Your branch is ahead of" in status)


def _clone(config, project):
    directory = config['management']['directory']
    project_directory = f"{directory}/{project['namespace']}/{project['name']}"
    if not os.path.isdir(project_directory):
        _git(f"git clone {project['ssh']} {project_directory}")


def _pull(config, project):
    directory = config['management']['directory']
    default_branch = config['git']['default_branch']
    project_directory = f"{directory}/{project['namespace']}/{project['name']}"
    current_branch = _git(f"git -C {project_directory} branch --show-current").rstrip()
    if current_branch == default_branch:
        status = _git(f"git -C {project_directory} status").rstrip()
        if _is_clear(status):
            _git(f"git -C {project_directory} pull")


if __name__ == "__main__":
    configuration = read_configuration()
    projects = create_store(Storage.PICKLE).load({}, configuration['project']['group_id'])
    CountableProcessor(lambda x: _clone(configuration, x), strategy=ExceptionStrategy.PASS).run(projects)
    CountableProcessor(lambda x: _pull(configuration, x), strategy=ExceptionStrategy.PASS).run(projects)
