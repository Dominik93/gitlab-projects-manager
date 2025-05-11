import os
import re
from functools import reduce

from configuration_reader import read_configuration
from count_executor import provide_countable
from store import get


def _search_in_project(directory: str, project_namespace: str, text: str, file_extension: str):
    project_directory = f"{directory}/{project_namespace}"
    results = []
    for (dirpath, dirnames, filenames) in os.walk(project_directory):
        for file in list(filter(lambda x: file_extension is None or file_extension in x, filenames)):
            path = dirpath + '/' + file
            print(f'Search {path}')
            f = open(path, "r", encoding="utf8")
            file_content = f.read()
            f.close()
            hit = re.search(text, file_content)
            if hit is not None:
                results.append(path)
    return results


def search(directory, projects, text, file_extension=None):
    results = provide_countable(projects, lambda x: _search_in_project(directory, x, text, file_extension))
    return reduce(list.__add__, results)


if __name__ == "__main__":
    configuration = read_configuration()
    directory = configuration['management']['directory']
    projects = list(map(lambda x: f"{directory}/{x['namespace']}/{x['name']}", get(configuration['group_id'])))
    print(search(directory, projects, "", ""))
