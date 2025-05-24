import base64
import json
from urllib.request import Request, urlopen

from commons.logger import Level, log


class GitlabAccessor:

    def __init__(self, url: str, token: str):
        self.base_url = url
        self.token = token

    def get_file(self, project_id, file):
        url_template = '/api/v4/projects/{project_id}/repository/files/{file}?ref=master'
        url = self._get_full_url(url_template.replace("{project_id}", str(project_id)).replace("{file}", file))
        response = self._execute_request(url)
        return base64.standard_b64decode(response["content"])

    def get_all_projects(self, group_id: str) -> list:
        projects_pages = []
        page = 1
        project_page = self._get_projects_page(group_id, page)
        projects_pages.extend(project_page)
        while len(project_page) == 100:
            page = page + 1
            project_page = self._get_projects_page(group_id, page)
            projects_pages.extend(project_page)
        return projects_pages

    def _get_projects_page(self, group_id: str, page: int):
        url_template = '/api/v4/groups/{groupId}/projects?include_subgroups=true&page={page}&per_page=100'
        url = self._get_full_url(url_template.replace("{groupId}", group_id).replace("{page}", str(page)))
        return self._execute_request(url)

    def _get_full_url(self, url: str):
        return self.base_url + url

    @log(Level.DEBUG, end_message=None)
    def _execute_request(self, url):
        req = Request(url)
        req.add_header('PRIVATE-TOKEN', self.token)
        content = urlopen(req).read()
        return json.loads(content)
