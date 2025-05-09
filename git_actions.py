import os

from configuration_reader import read_configuration
from store import get


def _count_executor(items, executor):
    i = 0
    total = len(items)
    for item in items:
        executor(item)
        i += 1
        print(f'Executed {i}/{total}')


def _clone(config, project):
    directory = config['management']['directory']
    project_directory = f"{directory}/{project['namespace']}/{project['name']}"
    command = f"git clone {project['ssh']} {project_directory}"
    print(f'Execute {command}')
    os.popen(command).read()


def _pull(config, project):
    directory = config['management']['directory']
    project_directory = f"{directory}/{project['namespace']}/{project['name']}"
    command = f"git -C {project_directory} branch --show-current"
    print(f'Execute {command}')
    current_branch = os.popen(command).read().rstrip()
    if current_branch == 'master':
        command = f"git -C {project_directory} pull"
        print(f'Execute {command}')
    os.popen(command).read()


if __name__ == "__main__":
    configuration = read_configuration()
    projects = get(configuration['group_id'])
    _count_executor(projects, lambda x: _clone(configuration, x))
    _count_executor(projects, lambda x: _pull(configuration, x))
