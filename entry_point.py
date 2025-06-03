from commons.configuration_reader import read_configuration
from commons.countable_processor import CountableProcessor, ExceptionStrategy
from commons.logger import get_logger
from commons.store import create_store, Storage
from git_actions import pull, clone, status, push, create_branch
from gitlab_actions import process
from maven_actions import bump_dependency
from search import search, SearchConfiguration

logger = get_logger("EntryPoint")


def load_entry_point(group_id):
    logger.info("load", f"Load {group_id}")
    store = create_store(Storage.JSON)
    store.load(lambda: process(group_id), group_id)


def reload_entry_point(group_id):
    logger.info("reload", f"Load {group_id}")
    store = create_store(Storage.JSON)
    store.delete(group_id)
    store.load(lambda: process(group_id), group_id)


def pull_entry_point(group_id: str, project_filters: list):
    config = read_configuration("config")
    config_directory = config.get_value("management.directory")
    default_branch = config.get_value("git.default_branch")
    store = create_store(Storage.JSON)
    projects = store.get(group_id)
    for project_filter in project_filters:
        projects = project_filter(projects)
    logger.info("pull", f"pull projects: {list(map(lambda x: x['id'], projects))}")
    CountableProcessor(projects).run(lambda x: pull(config_directory, default_branch, x),
                                     exception_strategy=ExceptionStrategy.PASS)


def push_entry_point(group_id: str, project_filters: list):
    config = read_configuration("config")
    config_directory = config.get_value("management.directory")
    store = create_store(Storage.JSON)
    projects = store.get(group_id)
    for project_filter in project_filters:
        projects = project_filter(projects)
    logger.info("pull", f"push projects: {list(map(lambda x: x['id'], projects))}")
    CountableProcessor(projects).run(lambda x: push(config_directory, x),
                                     exception_strategy=ExceptionStrategy.PASS)


def clone_entry_point(group_id: str, project_filters: list):
    config = read_configuration("config")
    config_directory = config.get_value("management.directory")
    store = create_store(Storage.JSON)
    projects = store.get(group_id)
    for project_filter in project_filters:
        projects = project_filter(projects)
    logger.info("pull", f"clone projects: {list(map(lambda x: x['id'], projects))}")
    CountableProcessor(projects).run(lambda x: clone(config_directory, x),
                                     exception_strategy=ExceptionStrategy.PASS)


def status_entry_point(group_id: str, project_filters: list):
    config = read_configuration("config")
    config_directory = config.get_value("management.directory")
    store = create_store(Storage.JSON)
    projects = store.get(group_id)
    for project_filter in project_filters:
        projects = project_filter(projects)
    logger.info("status", f"check status of projects: {list(map(lambda x: x['id'], projects))}")
    return CountableProcessor(projects).run(lambda x: status(config_directory, x),
                                            exception_strategy=ExceptionStrategy.PASS)


def search_entry_point(group_id: str, project_filters: list, search_config: SearchConfiguration):
    config = read_configuration("config")
    directory = config.get_value("management.directory")
    store = create_store(Storage.JSON)
    projects = store.get(group_id)
    for project_filter in project_filters:
        projects = project_filter(projects)
    logger.info("search", f"search in {list(map(lambda x: x['id'], projects))} for {search_config}")
    return search(projects, directory, search_config)


def create_branch_entry_point(group_id, branch, project_filters):
    config = read_configuration("config")
    config_directory = config.get_value("management.directory")
    store = create_store(Storage.JSON)
    projects = store.get(group_id)
    for project_filter in project_filters:
        projects = project_filter(projects)
    logger.info("create_branch", f"create branch {branch} in : {list(map(lambda x: x['id'], projects))}")
    return CountableProcessor(projects).run(lambda x: create_branch(config_directory, branch, x),
                                            exception_strategy=ExceptionStrategy.PASS)


def bump_dependency_entry_point(group_id, dependency_name, dependency_version, project_filters):
    config = read_configuration("config")
    config_directory = config.get_value("management.directory")
    store = create_store(Storage.JSON)
    projects = store.get(group_id)
    for project_filter in project_filters:
        projects = project_filter(projects)
    logger.info("create_branch", f"bump {dependency_name} to {dependency_version} in: {projects}")
    return CountableProcessor(projects).run(
        lambda x: bump_dependency(config_directory, dependency_name, dependency_version, x),
        exception_strategy=ExceptionStrategy.PASS)
