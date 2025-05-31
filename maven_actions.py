import os

from commons.logger import log, Level


@log(Level.DEBUG, start_message="Execute {args}", end_message="Command executed {result} in {duration}ms")
def _maven(command):
    return os.popen(command).read().rstrip()


def bump_dependency(config, dependency: str, version: str, project: dict):
    directory = config['management']['directory']
    project_directory = f"{directory}/{project['namespace']}/{project['name']}"
    if not os.path.isdir(project_directory):
        _maven(
            f"mvn -f {project_directory} versions:update-property -Dproperty={dependency}.version -DnewVersion={version}")
