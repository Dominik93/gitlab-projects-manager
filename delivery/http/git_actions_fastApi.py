from fastapi import FastAPI
from pydantic import BaseModel

from commons.configuration_reader import read_configuration
from commons.countable_processor import ExceptionStrategy, CountableProcessor
from commons.logger import get_logger
from commons.store import create_store, Storage
from git_actions import pull
from project_filter import filter_projects


class Filter(BaseModel):
    projects_ids: list = []


app = FastAPI()

logger = get_logger("GitActionsFastAPI")


@app.get("/namespace/{group_id}/projects")
async def get_projects(group_id):
    logger.info("get_projects", f"GET projects  {group_id}")
    store = create_store(Storage.JSON)
    projects = store.get(group_id)
    return projects


@app.post("/namespace/{group_id}/pull")
async def post_pull(group_id, project_filter: Filter):
    logger.info("post_pull", f"POST pull {group_id} {project_filter}")
    config = read_configuration("config")
    config_directory = config.get_value("management.directory")
    store = create_store(Storage.JSON)
    projects = store.get(group_id)
    id_filter = {"id": None if len(project_filter.projects_ids) == 0 else project_filter.projects_ids}
    projects = filter_projects(projects, {}, id_filter)
    CountableProcessor(lambda x: pull(config_directory, x), strategy=ExceptionStrategy.PASS).run(projects)
