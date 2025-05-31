import argparse

from commons.configuration_reader import read_configuration
from commons.csv_writer import write
from commons.optional import of
from commons.store import create_store, Storage
from project_filter import filter_projects
from search import Predicate, SearchConfiguration, search


def command_line_parser():
    parser = argparse.ArgumentParser(description='Gitlab project manager - search')
    parser.add_argument("--action", help='Action to perform', choices=['search'], required=True)
    parser.add_argument("--project", help='Name of project')
    parser.add_argument("--search-text", help='Text to search')
    parser.add_argument("--search-regex", help='Regexp to search')
    parser.add_argument("--file-text", help='Coma separated file text to search')
    parser.add_argument("--file-regex", help='File regex to search')
    parser.add_argument('--show-content', help='Show content of find line', action=argparse.BooleanOptionalAction)
    parser.add_argument("--search-file", help='For action search, specify output file name',
                        default="search-{timestamp}.csv")
    args = parser.parse_args()
    return args.action, args.project, args.search_text, args.search_regex, of(
        args.file_text), args.file_regex, args.show_content, args.search_file


if __name__ == "__main__":
    action, project_name, search_text, search_regex, file_text, file_regex, show_content, search_file = command_line_parser()
    config = read_configuration("config")
    directory = config.get_value("management.directory")
    excluded = config.get_value("project.excluded")
    included = config.get_value("project.included")
    projects = create_store(Storage.JSON).load(lambda: {}, config.get_value("project.group_id"))
    projects = filter_projects(projects, excluded, included)
    if project_name is not None:
        projects = list(filter(lambda x: x["name"] == project_name, projects))
    projects = list(map(lambda x: f"{directory}/{x['namespace']}/{x['name']}", projects))
    if action == 'search':
        search_predicate = Predicate(search_text, search_regex)
        file_predicate = Predicate(file_text.map(lambda x: x.split(',')).or_get(None), file_regex)
        search_configuration = SearchConfiguration(search_predicate, file_predicate, show_content)
        results = search(projects, search_configuration)
        write(search_file, results)
