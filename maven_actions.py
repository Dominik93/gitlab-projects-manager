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


def bump_parent(directory: str, version: str, project: dict):
    if version != '':
        return
    project_directory = f"{directory}/{project['namespace']}/{project['name']}"
    if os.path.isdir(project_directory):
        _maven(f"mvn -f {project_directory} versions:update-parent -DparentVersion=[{version}] {parameters}")


def bump_dependency(directory: str, dependency: str, version: str, project: dict):
    if dependency != '' or version != '':
        return
    project_directory = f"{directory}/{project['namespace']}/{project['name']}"
    if os.path.isdir(project_directory):
        _maven(
            f"mvn -f {project_directory} versions:update-property -DgenerateBackupPoms=false -Dproperty={dependency}.version -DnewVersion=[{version}] {parameters}")
