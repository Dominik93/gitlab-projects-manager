import argparse

from commons.configuration_reader import read_configuration
from commons.countable_processor import CountableProcessor, ExceptionStrategy
from commons.csv_writer import write
from commons.logger import set_root_level, Level
from commons.store import create_store, Storage
from git_actions import clone, pull, create_branch, push, status
from project_filter import filter_projects

set_root_level(Level.DEBUG)


def command_line_parser():
    parser = argparse.ArgumentParser(description='Gitlab project manager - git')
    parser.add_argument("--action", choices=['clone', 'pull', 'push', 'create-branch', 'status'],
                        help='Action to perform', default='pull')
    parser.add_argument("--project-name", help='Name of project')
    parser.add_argument("--branch", help='Name of branch to create')
    parser.add_argument("--status-file", help='For action status, specify output file name',
                        default="status-{timestamp}.csv")
    args = parser.parse_args()
    return args.action, args.project_name, args.branch, args.status_file


if __name__ == "__main__":
    action, project_name, branch, status_file = command_line_parser()
    config = read_configuration("config")
    excluded = config.get_value("project.excluded")
    included = config.get_value("project.included")
    config_directory = config.get_value("management.directory")
    store = create_store(Storage.JSON)
    projects = store.load(lambda: {}, config.get_value("project.group_id"))
    projects = filter_projects(projects, excluded, included)
    if project_name is not None:
        projects = list(filter(lambda x: x["name"] == project_name, projects))
    strategy = ExceptionStrategy.PASS
    if action == 'clone':
        CountableProcessor(lambda x: clone(config_directory, x), strategy=strategy).run(projects)
    if action == 'pull':
        CountableProcessor(lambda x: pull(config_directory, x), strategy=strategy).run(projects)
    if action == 'push':
        CountableProcessor(lambda x: push(config_directory, x), strategy=strategy).run(projects)
    if action == 'create-branch':
        CountableProcessor(lambda x: create_branch(config_directory, branch, x), strategy=strategy).run(projects)
    if action == 'status':
        projects_statues = CountableProcessor(lambda x: status(config_directory, x), strategy=strategy).run(projects)
        store.store(projects, config.get_value("project.group_id"))
        write(status_file, projects_statues)
