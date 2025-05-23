import os

from configuration_reader import read_configuration
from commons.store import create_store, Storage
from commons.countable_processor import CountableProcessor, ExceptionStrategy


def _clone(config, project):
    directory = config['management']['directory']
    project_directory = f"{directory}/{project['namespace']}/{project['name']}"
    command = f"git clone {project['ssh']} {project_directory}"
    print(f'Execute {command}')
    os.popen(command).read()


def _is_clear(status):
    return not ("Changes to be committed" in status or
                "Changes not staged for commit:" in status or
                "Your branch is ahead of" in status)


def _pull(config, project):
    directory = config['management']['directory']
    default_branch = config['git']['default_branch']
    project_directory = f"{directory}/{project['namespace']}/{project['name']}"
    command = f"git -C {project_directory} branch --show-current"
    print(f'Execute {command}')
    current_branch = os.popen(command).read().rstrip()
    if current_branch == default_branch:
        command = f"git -C {project_directory} status"
        print(f'Execute {command}')
        status = os.popen(command).read().rstrip()
        if _is_clear(status):
            command = f"git -C {project_directory} pull"
            print(f'Execute {command}')
            os.popen(command).read()


if __name__ == "__main__":
    configuration = read_configuration()
    projects = create_store(Storage.PICKLE).load({}, configuration['project']['group_id'])

    CountableProcessor(lambda x: _clone(configuration, x), strategy=ExceptionStrategy.PASS).run(projects)
    CountableProcessor(lambda x: _pull(configuration, x), strategy=ExceptionStrategy.PASS).run(projects)
