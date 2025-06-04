import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from starlette.responses import HTMLResponse, JSONResponse
from starlette.staticfiles import StaticFiles

from commons.configuration_reader import read_configuration
from commons.countable_processor import ExceptionStrategy
from commons.optional import of
from commons.store import create_store, Storage
from entry_point import load_entry_point, reload_entry_point, pull_entry_point, clone_entry_point, status_entry_point, \
    search_entry_point, create_branch_entry_point, bump_dependency_entry_point, push_entry_point, commit_entry_point
from project_filter import filter_projects, create_id_filter
from search import SearchConfiguration, text_predicate, regexp_predicate


class Filter(BaseModel):
    projects_ids: list = []


class CommitReqeust(BaseModel):
    projects_ids: list = []
    message: str


class SearchRequest(BaseModel):
    projects_ids: list = []
    search_text: str = None
    search_regex: bool = False
    file_text: str = None
    file_regex: bool = False
    show_content: bool = False


class BumpDependencyRequest(BaseModel):
    projects_ids: list = []
    dependency: str
    version: str


class CreateBranchRequest(BaseModel):
    projects_ids: list = []
    branch: str


app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "http://localhost:4200",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get('/')
def get_app_angular():
    with open('static/index.html', 'r') as file_index:
        html_content = file_index.read()
    return HTMLResponse(html_content, status_code=200)


@app.post("/namespace/{group_id}", tags=['group'], operation_id="loadGroup")
async def post_load_group(group_id):
    try:
        load_entry_point(group_id)
    except Exception as e:
        return internal_server_error(e)


@app.patch("/namespace/{group_id}", tags=['group'], operation_id="reloadGroup")
async def patch_reload_group(group_id):
    try:
        reload_entry_point(group_id)
    except Exception as e:
        return internal_server_error(e)


@app.get("/namespace/{group_id}/projects", tags=['projects'], operation_id="getProjects")
async def get_projects(group_id):
    try:
        store = create_store(Storage.JSON)
        projects = store.get(group_id)
        providers = _get_blocked_providers()
        for project in projects:
            for key in providers:
                del project[key]
        return projects
    except Exception as e:
        return internal_server_error(e)


@app.post("/namespace/{group_id}/projects/push", tags=['git'], operation_id="push")
async def post_push(group_id, project_filter: Filter):
    try:
        push_entry_point(group_id, _get_projects_filters(project_filter.projects_ids), ExceptionStrategy.RAISE)
    except Exception as e:
        return internal_server_error(e)


@app.post("/namespace/{group_id}/projects/commit", tags=['git'], operation_id="commit")
async def post_commit(group_id, request: CommitReqeust):
    try:
        commit_entry_point(group_id, request.message, _get_projects_filters(request.projects_ids),
                           ExceptionStrategy.RAISE)
    except Exception as e:
        return internal_server_error(e)


@app.post("/namespace/{group_id}/projects/pull", tags=['git'], operation_id="pull")
async def post_pull(group_id, project_filter: Filter):
    try:
        pull_entry_point(group_id, _get_projects_filters(project_filter.projects_ids), ExceptionStrategy.RAISE)
    except Exception as e:
        return internal_server_error(e)


@app.post("/namespace/{group_id}/projects/clone", tags=['git'], operation_id="clone")
async def post_clone(group_id, project_filter: Filter):
    try:
        clone_entry_point(group_id, _get_projects_filters(project_filter.projects_ids), ExceptionStrategy.RAISE)
    except Exception as e:
        return internal_server_error(e)


@app.post("/namespace/{group_id}/projects/status", tags=['git'], operation_id="status")
async def post_status(group_id, project_filter: Filter):
    try:
        status_entry_point(group_id, _get_projects_filters(project_filter.projects_ids), ExceptionStrategy.RAISE)
    except Exception as e:
        return internal_server_error(e)


@app.post("/namespace/{group_id}/projects/search", tags=['file'], operation_id="search")
async def post_search(group_id, request: SearchRequest):
    try:
        search_predicate = (of(request.search_text)
                            .map(lambda x: regexp_predicate(x) if request.search_regex else text_predicate(x))
                            .or_else_throw())
        file_predicate = (of(request.file_text)
                          .map(lambda x: regexp_predicate(x) if request.search_regex else text_predicate(x.split(',')))
                          .or_get(None))
        search_configuration = SearchConfiguration(search_predicate, file_predicate, request.show_content)
        return search_entry_point(group_id, _get_projects_filters(request.projects_ids), search_configuration,
                                  ExceptionStrategy.RAISE)
    except Exception as e:
        return internal_server_error(e)


@app.post("/namespace/{group_id}/projects/branch", tags=['git'], operation_id="create_branch")
async def post_create_branch(group_id, request: CreateBranchRequest):
    try:
        return create_branch_entry_point(group_id, request.branch, _get_projects_filters(request.projects_ids),
                                         ExceptionStrategy.RAISE)
    except Exception as e:
        return internal_server_error(e)


@app.patch("/namespace/{group_id}/projects/bump-dependency", tags=['maven'], operation_id="bump_dependency")
async def patch_bump_dependency(group_id, request: BumpDependencyRequest):
    try:
        bump_dependency_entry_point(group_id, request.dependency, request.version,
                                    _get_projects_filters(request.projects_ids), ExceptionStrategy.RAISE)
    except Exception as e:
        return internal_server_error(e)


def _get_projects_filters(ids):
    return [lambda projects: filter_projects(projects, {}, create_id_filter(ids))]


def _get_blocked_providers():
    config = read_configuration("config")
    ui_providers = config.get_value("providers.ui")
    loader_providers = config.get_value("providers.loader")
    blocked_providers = set()
    for provider in loader_providers:
        if provider not in ui_providers:
            blocked_providers.add(provider)
    return blocked_providers


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)


def internal_server_error(e):
    return JSONResponse(status_code=500, content={"error": "Internal Server Error", "message": str(e)})
