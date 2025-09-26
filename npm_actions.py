import json
import os

from commons.logger import log, Level


@log(Level.DEBUG, start_message="Execute {args}", end_message="Command executed {result} in {duration}ms")
def _npm(command):
    command_result = os.popen(command).read().rstrip()
    if "ERROR" in command_result:
        raise Exception(f"Error while executing {command}")
    return command_result


def install(directory: str, project: dict):
    project_directory = f"{directory}/{project['namespace']}/{project['name']}"
    _npm(f'cd {project_directory} && npm i')


def version(directory: str, project: dict):
    package_json_file = _get_package_json_file(directory, project)
    with open(package_json_file, encoding='utf-8') as f:
        project_version = json.load(f)['version']
    project['version'] = project_version
    return project


def bump_dependency(directory: str, dependency: str, version: str, project: dict):
    if dependency == '' or version == '':
        return
    package_json_file = _get_package_json_file(directory, project)
    with open(package_json_file, encoding='utf-8') as f:
        package_json = json.load(f)['version']
    if dependency in package_json['dependencies']:
        package_json['dependencies'][dependency] = version
    if dependency in package_json['devDependencies']:
        package_json['devDependencies'][dependency] = version

    with open(package_json_file, 'w', encoding='utf-8') as f:
        json.dump(package_json, f, ensure_ascii=False, indent=2)

    install(directory, project)


def _get_package_json_file(directory, project):
    project_directory = f"{directory}/{project['namespace']}/{project['name']}"
    package_json_file = f'{project_directory}/package.json'
    return package_json_file
