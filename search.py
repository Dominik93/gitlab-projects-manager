import os
import re
from functools import reduce

from commons.countable_processor import CountableProcessor
from commons.logger import log, Level
from commons.store import create_store, Storage
from configuration_reader import read_configuration

EXCLUDED = ['.git']


def _hit(text, regexp, content):
    if text is not None:
        return text in content
    if regexp is not None:
        return re.search(regexp, content)
    return Exception("Text and regexp are None")


def _search_in_project(project_directory: str, text: str = None,
                       regexp: str = None, file_extension: str = None) -> list[str]:
    hits = []
    for (dirpath, dirnames, filenames) in os.walk(project_directory):
        dirnames[:] = list(filter(lambda x: x not in EXCLUDED, dirnames))
        for file in list(filter(lambda x: file_extension is None or file_extension in x, filenames)):
            path = dirpath + '/' + file
            file_content = _read(path)
            if _hit(text, regexp, file_content):
                hits.append(path)
    return hits


@log(level=Level.DEBUG, start_message="Search {args}")
def _read(path):
    f = open(path, "r", encoding="utf8")
    file_content = f.read()
    f.close()
    return file_content


def _apply_filter(projects):
    filtered_projects = list(filter(lambda x: x, projects))
    return filtered_projects


def search(paths: list, text: str = None, regexp: str = None, file_extension: str = None):
    search_results = CountableProcessor(lambda x: _search_in_project(x, text, regexp, file_extension)).run(paths)
    return reduce(list.__add__, search_results)


if __name__ == "__main__":
    configuration = read_configuration()
    directory = configuration['management']['directory']
    projects = create_store(Storage.PICKLE).load({}, configuration['project']['group_id'])
    projects = _apply_filter(projects)
    projects = list(map(lambda x: f"{directory}/{x['namespace']}/{x['name']}", projects))
    results = search(projects, "", "", "")
    print(*results, sep='\n')
