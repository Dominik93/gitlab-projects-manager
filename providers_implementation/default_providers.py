from providers.providers_registry import add_provider


@add_provider('namespace')
def namespace_provider(project):
    return project['path_with_namespace'].rsplit('/', 1)[0]


@add_provider('ssh')
def ssh_provider(project):
    return project['ssh_url_to_repo']


@add_provider('id')
def ssh_provider(project):
    return project['id']


@add_provider('archived')
def archived_provider(project):
    return project['archived']


@add_provider('name')
def name_provider(project):
    return project['name']


@add_provider('url')
def url_provider(project):
    return project['web_url']
