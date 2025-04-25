from gitlab_accessor import GitlabAccessor
from providers.providers_registry import providers_registry
from providers_implementation.providers_impl import *


def process(providers: list[str], pages: list[list[dict]]) -> list[dict]:
    projects = []
    for page in pages:
        for project in page:
            projects.append(process_project(providers, project))
    return projects


def process_project(providers: list[str], gitlab_project: dict) -> dict:
    project = {'name': gitlab_project['name'], 'archived': gitlab_project["archived"]}

    for provider in providers:
        project[provider] = providers_registry[provider](gitlab_project)
    return project


if __name__ == "__main__":
    configuration = read_configuration()
    accessor = GitlabAccessor(configuration['gitlab_url'], configuration['access_token'])
    projects_pages = accessor.get_all_projects(configuration['group_id'])
    print(process(configuration['providers'], projects_pages))
