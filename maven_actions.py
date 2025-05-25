import os

from commons.configuration_reader import read_configuration
from commons.countable_processor import CountableProcessor, ExceptionStrategy
from commons.logger import log, Level
from commons.store import create_store, Storage
from project_filter import filter_projects


@log(Level.DEBUG, start_message="Execute {args}", end_message="Command executed {result} in {duration}ms")
def _maven(command):
    return os.popen(command).read().rstrip()


def bump_dependency(config, dependency: str, version: str, project: dict):
    directory = config['management']['directory']
    project_directory = f"{directory}/{project['namespace']}/{project['name']}"
    if not os.path.isdir(project_directory):
        _maven(
            f"mvn -f {project_directory} versions:update-property -Dproperty={dependency}.version -DnewVersion={version}")


if __name__ == "__main__":
    config = read_configuration("config")
    excluded = config.get_value("project.excluded")
    included = config.get_value("project.included")
    projects = create_store(Storage.JSON).load({}, config.get_value("project_id"))
    projects = filter_projects(projects, excluded, included)
    CountableProcessor(lambda x: bump_dependency(config, "", "", x), strategy=ExceptionStrategy.PASS).run(
        projects)
