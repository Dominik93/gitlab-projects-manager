import argparse

from commons.configuration_reader import read_configuration
from commons.store import create_store, Storage
from gitlab_accessor import GitlabAccessor
from gitlab_projects_manager import process


def command_line_parser():
    parser = argparse.ArgumentParser(description='Gitlab project manager - main')
    args = parser.parse_args()
    return None


if __name__ == "__main__":
    command_line_parser()
    configuration = read_configuration("config")
    accessor = GitlabAccessor(configuration.get_value("git.url"), configuration.get_value("git.access_token"))
    group_id = configuration.get_value("project.group_id")
    projects_pages = accessor.get_all_projects(group_id)
    providers = configuration.get_value("providers")
    projects = create_store(Storage.JSON).load(lambda: process(providers, projects_pages), group_id)
