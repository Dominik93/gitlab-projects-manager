import os

from commons.configuration_manager import read_configuration
from commons.countable_processor import CountableProcessor, ExceptionStrategy
from commons.lists import partition, flat
from commons.logger import get_logger
from commons.store import create_store, Storage
from commons.executor import AsyncExecutor
from git_actions import pull, clone, status, push, create_branch, commit, checkout, rollback
from gitlab_actions import process
from maven_actions import bump_dependency
from search import search, SearchConfiguration

PARTITION_SIZE = 50

logger = get_logger("EntryPoint")


def get_namespaces_entry_point():
    logger.info("get", f"Get namespaces")
    return _directory_files('resources/namespace')


def load_namespace_entry_point(name: str, group_id: str):
    logger.info("load", f"Load {group_id}")
    store = create_store(Storage.JSON)
    store.load(lambda: process(group_id), f'resources/namespace/{name}')


def delete_namespace_entry_point(name):
    logger.info("delete", f"Delete {name}")
    store = create_store(Storage.JSON)
    store.delete(f'resources/namespace/{name}')


def get_namespace_projects_entry_point(name):
    store = create_store(Storage.JSON)
    return store.get(f'resources/namespace/{name}')['projects']


def get_namespace_id_entry_point(name):
    store = create_store(Storage.JSON)
    return store.get(f'resources/namespace/{name}')['id']


def pull_entry_point(name: str, project_filters: list, exception_strategy: ExceptionStrategy):
    config = read_configuration("config")
    config_directory = config.get_value("management.directory")
    default_branch = config.get_value("git.default_branch")
    projects = get_namespace_projects_entry_point(name)
    projects = _filter_projects(project_filters, projects)
    logger.info("pull", f"pull projects: {list(map(lambda project: project['id'], projects))}")
    async_executor = AsyncExecutor()
    for items in partition(projects, PARTITION_SIZE):
        async_executor.add(_pull_entry_point, [items, config_directory, default_branch, exception_strategy])
    async_executor.execute()


def _pull_entry_point(projects: list, config_directory: str, default_branch: str,
                      exception_strategy: ExceptionStrategy):
    CountableProcessor(projects).run(lambda project: pull(config_directory, default_branch, project),
                                     exception_strategy=exception_strategy)


def checkout_entry_point(name: str, project_filters: list, exception_strategy: ExceptionStrategy):
    config = read_configuration("config")
    config_directory = config.get_value("management.directory")
    default_branch = config.get_value("git.default_branch")
    projects = get_namespace_projects_entry_point(name)
    projects = _filter_projects(project_filters, projects)
    logger.info("checkout", f"checkout projects: {list(map(lambda project: project['id'], projects))}")
    CountableProcessor(projects).run(lambda project: checkout(config_directory, default_branch, project),
                                     exception_strategy=exception_strategy)


def rollback_entry_point(name: str, project_filters: list, exception_strategy: ExceptionStrategy):
    config = read_configuration("config")
    config_directory = config.get_value("management.directory")
    projects = get_namespace_projects_entry_point(name)
    projects = _filter_projects(project_filters, projects)
    logger.info("rollback", f"rollback projects: {list(map(lambda project: project['id'], projects))}")
    CountableProcessor(projects).run(lambda project: rollback(config_directory, project),
                                     exception_strategy=exception_strategy)


def commit_entry_point(name: str, message: str, project_filters: list, exception_strategy: ExceptionStrategy):
    config = read_configuration("config")
    config_directory = config.get_value("management.directory")
    projects = get_namespace_projects_entry_point(name)
    projects = _filter_projects(project_filters, projects)
    logger.info("commit", f"commit with {message} into projects: {list(map(lambda project: project['id'], projects))}")
    CountableProcessor(projects).run(lambda project: commit(config_directory, message, project),
                                     exception_strategy=exception_strategy)


def push_entry_point(name: str, project_filters: list, exception_strategy: ExceptionStrategy):
    config = read_configuration("config")
    config_directory = config.get_value("management.directory")
    projects = get_namespace_projects_entry_point(name)
    projects = _filter_projects(project_filters, projects)
    logger.info("push", f"push projects: {list(map(lambda project: project['id'], projects))}")
    CountableProcessor(projects).run(lambda project: push(config_directory, project),
                                     exception_strategy=exception_strategy)


def clone_entry_point(name: str, project_filters: list, exception_strategy: ExceptionStrategy):
    config = read_configuration("config")
    config_directory = config.get_value("management.directory")
    store = create_store(Storage.JSON)
    projects = get_namespace_projects_entry_point(name)
    group_id = get_namespace_id_entry_point(name)
    filtered_projects = _filter_projects(project_filters, projects)
    logger.info("clone", f"clone projects: {list(map(lambda project: project['id'], filtered_projects))}")

    async_executor = AsyncExecutor()
    for items in partition(filtered_projects, PARTITION_SIZE):
        async_executor.add(_clone_entry_point, [items, config_directory, exception_strategy])
    processed_projects = flat(async_executor.execute())

    for project in projects:
        for processed_project in processed_projects:
            if project["id"] == processed_project["id"]:
                project["cloned"] = processed_project["cloned"]
    store.store({"id": group_id, "projects": projects}, f'resources/namespace/{name}')
    return processed_projects


def _clone_entry_point(projects: list, config_directory: str, exception_strategy: ExceptionStrategy):
    return CountableProcessor(projects).run(lambda project: clone(config_directory, project),
                                     exception_strategy=exception_strategy)


def status_entry_point(name: str, project_filters: list, exception_strategy: ExceptionStrategy):
    config = read_configuration("config")
    config_directory = config.get_value("management.directory")
    store = create_store(Storage.JSON)
    projects = get_namespace_projects_entry_point(name)
    group_id = get_namespace_id_entry_point(name)
    filtered_projects = _filter_projects(project_filters, projects)
    logger.info("status", f"check status of projects: {list(map(lambda project: project['id'], filtered_projects))}")

    async_executor = AsyncExecutor()
    for items in partition(filtered_projects, PARTITION_SIZE):
        async_executor.add(_status_entry_point, [items, config_directory, exception_strategy])
    processed_projects = flat(async_executor.execute())

    for project in projects:
        for processed_project in processed_projects:
            if project["id"] == processed_project["id"]:
                project["current_branch"] = processed_project["current_branch"]
                project["local_changes"] = processed_project["local_changes"]
    store.store({"id": group_id, "projects": projects}, f'resources/namespace/{name}')
    return processed_projects


def _status_entry_point(projects: list, config_directory: str, exception_strategy: ExceptionStrategy):
    return CountableProcessor(projects).run(lambda project: status(config_directory, project),
                                            exception_strategy=exception_strategy)


def get_search_results_entry_point(name: str):
    logger.info("get_search_results", f"Get search results {name}")
    return _directory_files(f'resources/search/{name}')


def get_search_result_entry_point(name: str, result: str):
    logger.info("get_search_result", f"Get search result {name}, {result}")
    store = create_store(Storage.JSON)
    return store.get(f'resources/search/{name}/{result}')


def search_entry_point(name: str, file_name: str, project_filters: list, search_config: SearchConfiguration,
                       exception_strategy: ExceptionStrategy):
    config = read_configuration("config")
    directory = config.get_value("management.directory")
    projects = get_namespace_projects_entry_point(name)
    projects = _filter_projects(project_filters, projects)
    logger.info("search", f"search in {list(map(lambda project: project['id'], projects))} for {search_config}")
    search_result = search(projects, directory, search_config, exception_strategy)
    if not os.path.exists(f'resources/search/{name}'):
        os.makedirs(f'resources/search/{name}')
    store = create_store(Storage.JSON)
    store.load(lambda: {"metadata": f"Search for {search_config}", "hits": search_result},
               f'resources/search/{name}/{file_name}')
    return search_result


def create_branch_entry_point(name: str, branch: str, project_filters: list, exception_strategy: ExceptionStrategy):
    config = read_configuration("config")
    config_directory = config.get_value("management.directory")
    projects = get_namespace_projects_entry_point(name)
    projects = _filter_projects(project_filters, projects)
    logger.info("create_branch", f"create branch {branch} in : {list(map(lambda project: project['id'], projects))}")
    return CountableProcessor(projects).run(lambda project: create_branch(config_directory, branch, project),
                                            exception_strategy=exception_strategy)


def bump_dependency_entry_point(name: str, dependency_name: str, dependency_version: str, project_filters: list,
                                exception_strategy: ExceptionStrategy):
    config = read_configuration("config")
    directory = config.get_value("management.directory")
    projects = get_namespace_projects_entry_point(name)
    projects = _filter_projects(project_filters, projects)
    logger.info("bump_dependency",
                f"bump {dependency_name} to {dependency_version} in: {list(map(lambda project: project['id'], projects))}")
    return CountableProcessor(projects).run(
        lambda project: bump_dependency(directory, dependency_name, dependency_version, project),
        exception_strategy=exception_strategy)


def _filter_projects(project_filters, projects):
    for project_filter in project_filters:
        projects = project_filter(projects)
    return projects


def _directory_files(directory: str):
    if os.path.isdir(directory):
        files = os.listdir(directory)
        return list(map(lambda x: os.path.splitext(x)[0], list(filter(lambda x: '.json' in x, files))))
    return []
