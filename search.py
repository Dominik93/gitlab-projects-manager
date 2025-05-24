import os
import re
from functools import reduce

from commons.countable_processor import CountableProcessor
from commons.csv_writer import write
from commons.logger import log, Level
from commons.optional import Optional, of, empty
from commons.store import create_store, Storage
from configuration_reader import read_configuration

EXCLUDED = ['.git']


class SearchConfiguration:

    def __init__(self, text: str = None, regexp: str = None, show_content: bool = None, file_extension: str = None):
        self.text = text
        self.regexp = regexp
        self.show_content = show_content
        self.file_extension = file_extension


def _find_line(text: str, regexp: str, content: str):
    for line in content.split("\n"):
        if _hit(text, regexp, line):
            return line.strip()
    raise Exception(f"Line with text {text} not found in content.")


def _hit(text: str, regexp: str, content: str) -> bool | None | Exception:
    if text is not None:
        return text in content
    if regexp is not None:
        return re.search(regexp, content)
    return Exception("Text and regexp are None")


def _search_in_project(project_directory: str, config: SearchConfiguration) -> list:
    hits = []
    for (dirpath, dirnames, filenames) in os.walk(project_directory):
        dirnames[:] = _filter_directories(dirnames)
        for file in _filter_files(filenames, config):
            path = dirpath + '/' + file
            file_content = _read(path)
            _get_hit(config, path, file_content).if_present(lambda x: hits.append(x))
    return hits


def _get_hit(config, path, file_content) -> Optional:
    if _hit(config.text, config.regexp, file_content):
        content = None
        if config.show_content:
            content = _find_line(config.text, config.regexp, file_content)
        return of({"file": path, "content": content})
    return empty()


def _filter_files(filenames, config):
    return list(filter(lambda x: config.file_extension is None or config.file_extension in x, filenames))


def _filter_directories(dirnames):
    return list(filter(lambda x: x not in EXCLUDED, dirnames))


@log(level=Level.DEBUG, start_message="Search {args}", end_message=None)
def _read(path):
    f = open(path, "r", encoding="utf8")
    file_content = f.read()
    f.close()
    return file_content


def _apply_filter(projects):
    filtered_projects = list(filter(lambda x: x, projects))
    return filtered_projects


def search(paths: list, config: SearchConfiguration):
    search_results = CountableProcessor(lambda x: _search_in_project(x, config)).run(paths)
    return reduce(list.__add__, search_results)


if __name__ == "__main__":
    configuration = read_configuration()
    directory = configuration['management']['directory']
    projects = create_store(Storage.PICKLE).load({}, configuration['project']['group_id'])
    projects = _apply_filter(projects)
    projects = list(map(lambda x: f"{directory}/{x['namespace']}/{x['name']}", projects))
    results = search(projects, SearchConfiguration("", "", False, ""))
    print(*results, sep='\n')
    write("search.csv", results)
