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

    def predicate(self, content: str) -> bool | None | Exception:
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
        if self.config.text_predicate.predicate(self.content):
            content = None
            if self.config.show_content:
                content = self._find_line(self.config.text_predicate)
            return of({"identifier": identifier, "content": content})
        return empty()

    def _find_line(self, predicate: Predicate):
        for line in self.content.split("\n"):
            if predicate.predicate(line):
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


def _filter_files(config, filenames):
    predicate = config.file_predicate
    return list(filter(lambda x: predicate is None or predicate.predicate(x), filenames))


def _filter_directories(dirnames):
    return list(filter(lambda x: x not in EXCLUDED, dirnames))


def search(paths: list, config: SearchConfiguration):
    search_results = CountableProcessor(lambda x: _search_in_project(x, config)).run(paths)
    return reduce(list.__add__, search_results)


if __name__ == "__main__":
    configuration = read_configuration("config")
    directory = configuration['management']['directory']
    project = configuration['project']
    excluded = project['excluded']
    included = project['included']
    projects = create_store(Storage.JSON).load({}, project['group_id'])
    projects = filter_projects(projects, excluded, included)
    projects = list(map(lambda x: f"{directory}/{x['namespace']}/{x['name']}", projects))
    results = search(projects, SearchConfiguration(text_predicate(""), regexp_predicate(""), False))
    print(*results, sep='\n')
    write("search-{timestamp}.csv", results)
