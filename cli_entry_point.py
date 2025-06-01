import argparse

from commons.configuration_reader import read_configuration
from commons.countable_processor import CountableProcessor, ExceptionStrategy
from commons.csv_writer import write
from commons.logger import set_root_level, Level
from commons.optional import of
from commons.store import create_store, Storage
from git_actions import clone, pull, create_branch, push, status
from gitlab_accessor import GitlabAccessor
from gitlab_actions import process
from maven_actions import bump_dependency
from project_filter import filter_projects
from search import Predicate, SearchConfiguration, search

set_root_level(Level.DEBUG)


def command_line_parser():
    parser = argparse.ArgumentParser(description='Gitlab project manager')
    parser.add_argument("--action",
                        choices=['load', 'clone', 'pull', 'push', 'create-branch', 'status', 'search',
                                 'bump-dependency'],
                        help='Action to perform', default='pull')
    parser.add_argument("--project-name", help='Name of project')

    parser.add_argument("--branch", help='Action: create-branch - Name of branch to create')
    parser.add_argument("--status-file", help='Action: status - Specify output file name',
                        default="status-{timestamp}.csv")

    parser.add_argument("--search-text", help='Action: search - Text to search')
    parser.add_argument("--search-regex", help='Action: search - Regexp to search')
    parser.add_argument("--file-text", help='Action: search - Coma separated file text to search')
    parser.add_argument("--file-regex", help='Action: search - File regex to search')
    parser.add_argument('--show-content', help='Action: search - Show content of find line',
                        action=argparse.BooleanOptionalAction)
    parser.add_argument("--search-file", help='Action: search - For action search, specify output file name',
                        default="search-{timestamp}.csv")

    parser.add_argument("--dependency-name", help='Action: bump-dependency - Dependency name')
    parser.add_argument("--dependency-version", help='Action: bump-dependency - Dependency version')
    return parser.parse_args()


def get_projects(store, group_id, project_name):
    projects = store.get(config.get_value(group_id))
    projects = filter_projects(projects, excluded, included)
    if project_name is not None:
        projects = list(filter(lambda project: project["name"] == project_name, projects))
    return projects


if __name__ == "__main__":
    args = command_line_parser()
    config = read_configuration("config")
    group_id = config.get_value("project.group_id")
    excluded = config.get_value("project.excluded")
    included = config.get_value("project.included")
    directory = config.get_value("management.directory")
    strategy = ExceptionStrategy.PASS
    store = create_store(Storage.JSON)
    if args.action == 'load':
        accessor = GitlabAccessor(config.get_value("git.url"), config.get_value("git.access_token"))
        projects_pages = accessor.get_all_projects(group_id)
        providers = config.get_value("providers")
        store.load(lambda: process(providers, projects_pages), group_id)

    projects = get_projects(store, group_id, args.project_name)
    if args.action == 'bump-dependency':
        CountableProcessor(
            lambda project: bump_dependency(config, args.dependency_name, args.dependency_version, project),
            strategy=strategy).run(projects)
    if args.action == 'search':
        projects = list(map(lambda project: f"{directory}/{project['namespace']}/{project['name']}", projects))
        search_predicate = Predicate(args.search_text, args.search_regex)
        file_predicate = Predicate(of(args.file_text).map(lambda x: x.split(',')).or_get(None), args.file_regex)
        search_configuration = SearchConfiguration(search_predicate, file_predicate, args.show_content)
        results = search(projects, search_configuration)
        write(args.search_file, results)
    if args.action == 'clone':
        CountableProcessor(lambda project: clone(directory, project), strategy=strategy).run(projects)
    if args.action == 'pull':
        CountableProcessor(lambda project: pull(directory, project), strategy=strategy).run(projects)
    if args.action == 'push':
        CountableProcessor(lambda project: push(directory, project), strategy=strategy).run(projects)
    if args.action == 'create-branch':
        CountableProcessor(lambda project: create_branch(directory, args.branch, project),
                           strategy=strategy).run(projects)
    if args.action == 'status':
        projects_statues = CountableProcessor(lambda project: status(directory, project), strategy=strategy).run(
            projects)
        store.store(projects, config.get_value("project.group_id"))
        write(args.status_file, projects_statues)
