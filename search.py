import argparse
import os
import re
from functools import reduce

from commons.configuration_reader import read_configuration
from commons.countable_processor import CountableProcessor
from commons.csv_writer import write
from commons.logger import log, Level
from commons.optional import Optional, of, empty
from commons.store import create_store, Storage
from project_filter import filter_projects

EXCLUDED = ['.git']


def text_predicate(text):
    return Predicate(text, None)


def regexp_predicate(regexp):
    return Predicate(None, regexp)


class Predicate:

    def __init__(self, text: str = None, regexp: str = None):
        self.text = text
        self.regexp = regexp

    def test(self, content: str) -> bool | None | Exception:
        if self.text is not None:
            return self.text in content
        if self.regexp is not None:
            return re.search(self.regexp, content)
        raise Exception("Text and regexp are None")


class SearchConfiguration:

    def __init__(self, text_predicate: Predicate = None, file_predicate: Predicate = None, show_content: bool = None):
        self.text_predicate = text_predicate
        self.file_predicate = file_predicate
        self.show_content = show_content


class Hit:

    def __init__(self, config: SearchConfiguration, content: str):
        self.config = config
        self.content = content

    def get_hit(self, identifier) -> Optional:
        if self.config.text_predicate.test(self.content):
            content = None
            if self.config.show_content:
                content = self._find_line(self.config.text_predicate)
            return of({"identifier": identifier, "content": content})
        return empty()

    def _find_line(self, predicate: Predicate):
        for line in self.content.split("\n"):
            if predicate.test(line):
                return line.strip()
        raise Exception(f"Line with text {predicate} not found in content.")


@log(level=Level.DEBUG, start_message="Search {args}", end_message=None)
def _read(path):
    f = open(path, "r", encoding="utf8")
    file_content = f.read()
    f.close()
    return file_content


def _search_in_project(project_directory: str, config: SearchConfiguration) -> list:
    hits = []
    for (dirpath, dirnames, filenames) in os.walk(project_directory):
        dirnames[:] = _filter_directories(dirnames)
        for file in _filter_files(config, filenames):
            path = dirpath + '/' + file
            Hit(config, _read(path)).get_hit(path).if_present(lambda x: hits.append(x))
    return hits


def _filter_files(config: SearchConfiguration, filenames):
    predicate = config.file_predicate
    if predicate is None:
        return filenames
    return list(filter(lambda x: predicate.test(x), filenames))


def _filter_directories(dirnames):
    return list(filter(lambda x: x not in EXCLUDED, dirnames))


def search(paths: list, config: SearchConfiguration):
    search_results = CountableProcessor(lambda x: _search_in_project(x, config)).run(paths)
    return reduce(list.__add__, search_results, [])


def command_line_parser():
    parser = argparse.ArgumentParser(description='Gitlab project manager - search')
    parser.add_argument("--action", help='Action to perform', choices=['search'], required=True)
    parser.add_argument("--project", help='Name of project')
    parser.add_argument("--search-text", help='Text to search')
    parser.add_argument("--search-regex", help='Regexp to search')
    parser.add_argument("--file-text", help='File text to search')
    parser.add_argument("--file-regex", help='File regex to search')
    parser.add_argument('--show-content', help='Show content of find line', action=argparse.BooleanOptionalAction)
    parser.add_argument("--search-file", help='For action search, specify output file name',
                        default="search-{timestamp}.csv")
    args = parser.parse_args()
    return args.action, args.project, args.search_text, args.search_regex, args.file_text, args.file_regex, args.show_content, args.search_file


if __name__ == "__main__":
    action, project_name, search_text, search_regex, file_text, file_regex, show_content, search_file = command_line_parser()
    config = read_configuration("config")
    directory = config.get_value("management.directory")
    excluded = config.get_value("project.excluded")
    included = config.get_value("project.included")
    projects = create_store(Storage.JSON).load(lambda: {}, config.get_value("project_id"))
    projects = filter_projects(projects, excluded, included)
    if project_name is not None:
        projects = list(filter(lambda x: x["name"] == project_name, projects))
    projects = list(map(lambda x: f"{directory}/{x['namespace']}/{x['name']}", projects))
    if action == 'search':
        search_predicate = Predicate(search_text, search_regex)
        file_predicate = Predicate(file_text, file_regex)
        search_configuration = SearchConfiguration(search_predicate, file_predicate, show_content)
        results = search(projects, search_configuration)
        write(search_file, results)
