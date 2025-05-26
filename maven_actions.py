import argparse
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


def command_line_parser():
    parser = argparse.ArgumentParser(description='Gitlab project manager - maven')
    parser.add_argument("--action", help='Action to perform', choices=['bump-dependency'], required=True)
    parser.add_argument("--project", help='Name of project')
    parser.add_argument("--dependency-name", help='Dependency name')
    parser.add_argument("--dependency-version", help='Dependency version')
    args = parser.parse_args()
    return args.action, args.project, args.dependnecy_name, args.dependnecy_version


if __name__ == "__main__":
    action, project, dependency_name, dependency_version = command_line_parser()
    config = read_configuration("config")
    excluded = config.get_value("project.excluded")
    included = config.get_value("project.included")
    projects = create_store(Storage.JSON).load({}, config.get_value("project.group_id"))
    projects = filter_projects(projects, excluded, included)
    if project is not None:
        projects = list(filter(lambda x: x["name"] == project, projects))
    if action == 'bump-dependency':
        CountableProcessor(lambda x: bump_dependency(config, dependency_name, dependency_version, x),
                           strategy=ExceptionStrategy.PASS).run(projects)
