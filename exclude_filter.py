def filter_not_excluded_projects(excluded, projects):
    filtered_projects = []
    for project in projects:
        is_excluded = False
        for key in excluded:
            is_excluded = is_excluded or project[key] in excluded[key]
        if not is_excluded:
            filtered_projects.append(project)
    return filtered_projects
