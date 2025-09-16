import os

from commons.logger import log, Level


@log(Level.DEBUG, start_message="Execute {args}", end_message="Command executed {result} in {duration}ms")
def _maven(command):
    command_result = os.popen(command).read().rstrip()
    if "ERROR" in command_result:
        raise Exception(f"Error while executing {command}")
    return command_result


def bump_dependency(directory, dependency: str, version: str, project: dict):
    project_directory = f"{directory}/{project['namespace']}/{project['name']}"
    if os.path.isdir(project_directory):
        _maven(f"mvn -f {project_directory} versions:update-property -DgenerateBackupPoms=false -Dproperty={dependency}.version -DnewVersion={version}")
