from commons.configuration_reader import read_configuration
from commons.countable_processor import CountableProcessor
from commons.store import create_store, Storage
from gitlab_accessor import GitlabAccessor
from providers.providers_registry import providers_registry


# import providers, do not remove


def _process_project(providers: list[str], gitlab_project: dict) -> dict:
    project = {}
    for provider in providers:
        project[provider] = providers_registry[provider](gitlab_project)
    return project


def process(providers: list[str], pages: list[dict]) -> list[dict]:
    return CountableProcessor(lambda x: _process_project(providers, x)).run(pages)


if __name__ == "__main__":
    configuration = read_configuration("config")
    accessor = GitlabAccessor(configuration.get_value("git.url"), configuration.get_value("git.access_token"))
    group_id = configuration.get_value("project.group_id")
    projects_pages = accessor.get_all_projects(group_id)
    providers = configuration.get_value("providers")
    projects = create_store(Storage.JSON).load(lambda: process(providers, projects_pages), group_id)
    print(projects)
