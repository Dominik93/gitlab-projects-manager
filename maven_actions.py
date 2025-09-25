import os

from commons.configuration_manager import read_configuration
from commons.logger import log, Level

config = read_configuration("config")
parameters = config.get_value("maven.parameters")


@log(Level.DEBUG, start_message="Execute {args}", end_message="Command executed {result} in {duration}ms")
def _maven(command):
    command_result = os.popen(command).read().rstrip()
    if "ERROR" in command_result:
        raise Exception(f"Error while executing {command}")
    return command_result


def version(directory: str, project: dict):
    project_directory = f"{directory}/{project['namespace']}/{project['name']}"
    return _maven(f'mvn -f {project_directory} help:evaluate -Dexpression=project.version -q -DforceStdout')


def bump_parent(directory: str, version: str, project: dict):
    if version == '':
        return
    project_directory = f"{directory}/{project['namespace']}/{project['name']}"
    if os.path.isdir(project_directory):
        parent_version = f"-DparentVersion=[{version}]"
        _maven(f"mvn -f {project_directory} versions:update-parent {parent_version} {parameters}")


def bump_dependency(directory: str, dependency: str, version: str, project: dict):
    if dependency == '' or version == '':
        return
    project_directory = f"{directory}/{project['namespace']}/{project['name']}"
    if os.path.isdir(project_directory):
        property = f"-Dproperty={dependency}.version"
        new_version = f"-DnewVersion=[{version}]"
        _maven(f"mvn -f {project_directory} versions:update-property {property} {new_version} {parameters}")
