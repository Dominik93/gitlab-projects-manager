import argparse

from commons.configuration_manager import read_configuration
from commons.countable_processor import ExceptionStrategy
from commons.csv_writer import write
from commons.optional import of
from commons.store import create_store, Storage
from entry_point import load_namespace_entry_point, pull_entry_point, status_entry_point, \
    clone_entry_point, \
    search_entry_point, push_entry_point, create_branch_entry_point, bump_dependency_entry_point, \
    delete_namespace_entry_point
from project_filter import filter_projects, create_name_filter
from search import Predicate, SearchConfiguration

store = create_store(Storage.JSON)
config = read_configuration("config")
group_id = config.get_value("project.group_id")
excluded = config.get_value("project.excluded")
included = config.get_value("project.included")
default_branch = config.get_value("git.default_branch")
directory = config.get_value("management.directory")
strategy = ExceptionStrategy.PASS


def command_line_parser():
    parser = argparse.ArgumentParser(description='Gitlab project manager')
    parser.add_argument("--action",
                        choices=['load', 'delete', 'clone', 'pull', 'push', 'create-branch', 'status', 'search',
                                 'bump-dependency'],
                        help='Action to perform', required=True)
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


def _load(args):
    group_id = read_configuration("config").get_value("project.group_id")
    load_namespace_entry_point(group_id, group_id)


def _delete(args):
    delete_namespace_entry_point(read_configuration("config").get_value("project.group_id"))


def _clone(args):
    clone_entry_point(group_id, _get_projects_filters(args), ExceptionStrategy.PASS)


def _push(args):
    push_entry_point(group_id, _get_projects_filters(args), ExceptionStrategy.PASS)


def _pull(args):
    pull_entry_point(group_id, _get_projects_filters(args), ExceptionStrategy.PASS)


def _status(args):
    projects_statues = status_entry_point(group_id, _get_projects_filters(args), ExceptionStrategy.PASS)
    write(args.status_file, projects_statues)


def _search(args):
    search_predicate = Predicate(args.search_text, args.search_regex)
    file_predicate = Predicate(of(args.file_text).map(lambda x: x.split(',')).or_get(None), args.file_regex)
    search_configuration = SearchConfiguration(search_predicate, file_predicate, args.show_content)
    results = search_entry_point(group_id, args.search_file, _get_projects_filters(args), search_configuration,
                                 ExceptionStrategy.PASS)
    write(args.search_file, results)


def _bump_dependency(args):
    bump_dependency_entry_point(group_id, args.dependency_name, args.dependency_version, _get_projects_filters(args),
                                ExceptionStrategy.PASS)


def _create_branch(args):
    create_branch_entry_point(group_id, args.branch, _get_projects_filters(args), ExceptionStrategy.PASS)


actions = {
    "load": _load,
    "delete": _delete,
    "status": _status,
    "clone": _clone,
    "pull": _pull,
    "push": _push,
    "search": _search,
    "bump-dependency": _bump_dependency,
    "create-branch": _create_branch
}

if __name__ == "__main__":
    args = command_line_parser()
    actions[args.action](args)


def _get_projects_filters(args):
    return [
        lambda projects: filter_projects(projects, excluded, included),
        lambda projects: filter_projects(projects, {}, create_name_filter(args.project_name))
    ]
