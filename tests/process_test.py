import unittest

from gitlab_actions import process_pages

component = {
    '_links': {
        'cluster_agents': 'https://gitlab/api/v4/projects/34292/cluster_agents',
        'events': 'https://gitlab/api/v4/projects/34292/events',
        'issues': 'https://gitlab/api/v4/projects/34292/issues',
        'labels': 'https://gitlab/api/v4/projects/34292/labels',
        'members': 'https://gitlab/api/v4/projects/34292/members',
        'merge_requests': 'https://gitlab/api/v4/projects/34292/merge_requests',
        'repo_branches': 'https://gitlab/api/v4/projects/34292/repository/branches',
        'self': 'https://gitlab/api/v4/projects/34292'
    },
    'allow_merge_on_skipped_pipeline': None,
    'analytics_access_level': 'enabled',
    'archived': False,
    'auto_cancel_pending_pipelines': 'enabled',
    'auto_devops_deploy_strategy': 'continuous',
    'auto_devops_enabled': False,
    'autoclose_referenced_issues': True,
    'avatar_url': None,
    'build_git_strategy': 'fetch',
    'build_timeout': 3600,
    'builds_access_level': 'enabled',
    'can_create_merge_request_in': True,
    'ci_allow_fork_pipelines_to_run_in_parent_project': True,
    'ci_config_path': 'pipelines/.component.ci.yml@global-sector/local-sector/com/sector/cicd',
    'ci_default_git_depth': 20,
    'ci_delete_pipelines_in_seconds': None,
    'ci_forward_deployment_enabled': True,
    'ci_forward_deployment_rollback_allowed': True,
    'ci_id_token_sub_claim_components': [
        'project_path',
        'ref_type',
        'ref'
    ],
    'ci_job_token_scope_enabled': False,
    'ci_pipeline_variables_minimum_override_role': 'developer',
    'ci_push_repository_for_job_token_allowed': False,
    'ci_separated_caches': True,
    'container_expiration_policy': {
        'cadence': '1d',
        'enabled': False,
        'keep_n': 10,
        'name_regex': '.*',
        'name_regex_keep': None,
        'next_run_at': '2025-03-19T13:40:37.017Z',
        'older_than': '90d'
    },
    'container_registry_access_level': 'enabled',
    'container_registry_enabled': True,
    'container_registry_image_prefix': 'gitlab-registry/global-sector/local-sector/com/sector/components/com-component',
    'created_at': '2025-03-18T13:40:36.979Z',
    'creator_id': 1938,
    'default_branch': 'master',
    'description': None,
    'description_html': '',
    'emails_disabled': False,
    'emails_enabled': True,
    'empty_repo': False,
    'enforce_auth_checks_on_uploads': True,
    'environments_access_level': 'enabled',
    'feature_flags_access_level': 'enabled',
    'forking_access_level': 'enabled',
    'forks_count': 0,
    'group_runners_enabled': True,
    'http_url_to_repo': 'https://gitlab/global-sector/local-sector/com/sector/components/com-component.git',
    'id': 34292,
    'import_status': 'none',
    'import_type': None,
    'import_url': None,
    'infrastructure_access_level': 'enabled',
    'issue_branch_template': '',
    'issues_access_level': 'enabled',
    'issues_enabled': True,
    'jobs_enabled': True,
    'keep_latest_artifact': False,
    'last_activity_at': '2025-04-11T05:25:46.371Z',
    'lfs_enabled': True,
    'merge_commit_template': None,
    'merge_method': 'merge',
    'merge_requests_access_level': 'enabled',
    'merge_requests_enabled': True,
    'model_experiments_access_level': 'enabled',
    'model_registry_access_level': 'enabled',
    'monitor_access_level': 'enabled',
    'name': 'com-component',
    'name_with_namespace': 'Global Sector/ Local Sector / com / sector / components / com-component',
    'namespace': {
        'avatar_url': None,
        'full_path': 'global-sector/local-sector/com/sector/components',
        'id': 28059,
        'kind': 'group',
        'name': 'components',
        'parent_id': 26883,
        'path': 'components',
        'web_url': 'https://gitlab/groups/global-sector/local-sector/com/sector/components'
    },
    'only_allow_merge_if_all_discussions_are_resolved': False,
    'only_allow_merge_if_pipeline_succeeds': False,
    'open_issues_count': 0,
    'packages_enabled': True,
    'pages_access_level': 'private',
    'path': 'com-component',
    'path_with_namespace': 'global-sector/local-sector/com/sector/components/com-component',
    'printing_merge_request_link_enabled': True,
    'public_jobs': True,
    'readme_url': 'https://gitlab/global-sector/local-sector/com/sector/components/com-component/-/blob/master/README.adoc',
    'releases_access_level': 'enabled',
    'remove_source_branch_after_merge': True,
    'repository_access_level': 'enabled',
    'repository_object_format': 'sha1',
    'request_access_enabled': True,
    'resolve_outdated_diff_discussions': False,
    'restrict_user_defined_variables': True,
    'runner_token_expiration_interval': None,
    'runners_token': None,
    'security_and_compliance_access_level': 'private',
    'service_desk_address': '',
    'service_desk_enabled': True,
    'shared_runners_enabled': False,
    'shared_with_groups': [

    ],
    'snippets_access_level': 'enabled',
    'snippets_enabled': True,
    'squash_commit_template': None,
    'squash_option': 'default_off',
    'ssh_url_to_repo': 'ssh://git@gitlab:2222/global-sector/local-sector/com/sector/components/com-component.git',
    'star_count': 0,
    'suggestion_commit_message': None,
    'tag_list': [

    ],
    'topics': [

    ],
    'updated_at': '2025-04-11T05:25:46.371Z',
    'visibility': 'private',
    'warn_about_potentially_unwanted_characters': True,
    'web_url': 'https://gitlab/global-sector/local-sector/com/sector/components/com-component',
    'wiki_access_level': 'enabled',
    'wiki_enabled': True
}

module = {
    '_links': {
        'cluster_agents': 'https://gitlab/api/v4/projects/22789/cluster_agents',
        'events': 'https://gitlab/api/v4/projects/22789/events',
        'issues': 'https://gitlab/api/v4/projects/22789/issues',
        'labels': 'https://gitlab/api/v4/projects/22789/labels',
        'members': 'https://gitlab/api/v4/projects/22789/members',
        'merge_requests': 'https://gitlab/api/v4/projects/22789/merge_requests',
        'repo_branches': 'https://gitlab/api/v4/projects/22789/repository/branches',
        'self': 'https://gitlab/api/v4/projects/22789'
    },
    'allow_merge_on_skipped_pipeline': None,
    'analytics_access_level': 'enabled',
    'archived': False,
    'auto_cancel_pending_pipelines': 'enabled',
    'auto_devops_deploy_strategy': 'continuous',
    'auto_devops_enabled': False,
    'autoclose_referenced_issues': True,
    'avatar_url': None,
    'build_git_strategy': 'fetch',
    'build_timeout': 3600,
    'builds_access_level': 'enabled',
    'can_create_merge_request_in': True,
    'ci_allow_fork_pipelines_to_run_in_parent_project': True,
    'ci_config_path': 'pipelines/.module.ci.yml@global-sector/local-sector/com/sector/cicd',
    'ci_default_git_depth': 20,
    'ci_delete_pipelines_in_seconds': None,
    'ci_forward_deployment_enabled': True,
    'ci_forward_deployment_rollback_allowed': True,
    'ci_id_token_sub_claim_components': [
        'project_path',
        'ref_type',
        'ref'
    ],
    'ci_job_token_scope_enabled': False,
    'ci_pipeline_variables_minimum_override_role': 'maintainer',
    'ci_push_repository_for_job_token_allowed': False,
    'ci_separated_caches': True,
    'container_expiration_policy': {
        'cadence': '1d',
        'enabled': False,
        'keep_n': 10,
        'name_regex': '.*',
        'name_regex_keep': 'None',
        'next_run_at': '2023-06-21T08:36:28.413Z',
        'older_than': '90d'
    },
    'container_registry_access_level': 'enabled',
    'container_registry_enabled': True,
    'container_registry_image_prefix': 'gitlab-registry/global-sector/local-sector/com/sector/modules/domain/com-module',
    'created_at': '2023-06-20T06:24:46.077Z',
    'creator_id': 1,
    'default_branch': 'master',
    'description': '',
    'description_html': '',
    'emails_disabled': False,
    'emails_enabled': True,
    'empty_repo': False,
    'enforce_auth_checks_on_uploads': True,
    'environments_access_level': 'enabled',
    'feature_flags_access_level': 'enabled',
    'forking_access_level': 'enabled',
    'forks_count': 0,
    'group_runners_enabled': True,
    'http_url_to_repo': 'https://gitlab/global-sector/local-sector/com/sector/modules/domain/com-module.git',
    'id': 22789,
    'import_status': 'finished',
    'import_type': 'gitlab_project',
    'import_url': None,
    'infrastructure_access_level': 'enabled',
    'issue_branch_template': None,
    'issues_access_level': 'enabled',
    'issues_enabled': True,
    'jobs_enabled': True,
    'keep_latest_artifact': False,
    'last_activity_at': '2025-04-10T06:43:33.692Z',
    'lfs_enabled': True,
    'merge_commit_template': None,
    'merge_method': 'merge',
    'merge_requests_access_level': 'enabled',
    'merge_requests_enabled': True,
    'model_experiments_access_level': 'enabled',
    'model_registry_access_level': 'enabled',
    'monitor_access_level': 'enabled',
    'name': 'com-module',
    'name_with_namespace': 'Global Sector/ Local Sector / com / sector / modules / domain / com-module',
    'namespace': {
        'avatar_url': None,
        'full_path': 'global-sector/local-sector/com/sector/modules/domain',
        'id': 28405,
        'kind': 'group',
        'name': 'domain',
        'parent_id': 26884,
        'path': 'domain',
        'web_url': 'https://gitlab/groups/global-sector/local-sector/com/sector/modules/domain'
    },
    'only_allow_merge_if_all_discussions_are_resolved': False,
    'only_allow_merge_if_pipeline_succeeds': False,
    'open_issues_count': 0,
    'packages_enabled': True,
    'pages_access_level': 'private',
    'path': 'com-module',
    'path_with_namespace': 'global-sector/local-sector/com/sector/modules/domain/com-module',
    'printing_merge_request_link_enabled': True,
    'public_jobs': True,
    'readme_url': 'https://gitlab/global-sector/local-sector/com/sector/modules/domain/com-module/-/blob/master/README.adoc',
    'releases_access_level': 'enabled',
    'remove_source_branch_after_merge': True,
    'repository_access_level': 'enabled',
    'repository_object_format': 'sha1',
    'request_access_enabled': True,
    'resolve_outdated_diff_discussions': False,
    'restrict_user_defined_variables': False,
    'runner_token_expiration_interval': None,
    'runners_token': None,
    'security_and_compliance_access_level': 'private',
    'service_desk_address': None,
    'service_desk_enabled': False,
    'shared_runners_enabled': False,
    'shared_with_groups': [

    ],
    'snippets_access_level': 'enabled',
    'snippets_enabled': True,
    'squash_commit_template': None,
    'squash_option': 'default_off',
    'ssh_url_to_repo': 'ssh://git@gitlab:2222/global-sector/local-sector/com/sector/modules/domain/com-module.git',
    'star_count': 0,
    'suggestion_commit_message': None,
    'tag_list': [

    ],
    'topics': [

    ],
    'updated_at': '2025-04-10T06:43:33.692Z',
    'visibility': 'private',
    'warn_about_potentially_unwanted_characters': True,
    'web_url': 'https://gitlab/global-sector/local-sector/com/sector/modules/domain/com-module',
    'wiki_access_level': 'enabled',
    'wiki_enabled': True
}


class ProcessTestCase(unittest.TestCase):
    def test_process(self):
        providers = ['id', 'name', 'archived', 'ssh', 'url', 'namespace']
        projects = process_pages(providers, [module, component])

        module_project = {'id': 22789,
                          'archived': False,
                          'namespace': 'global-sector/local-sector/com/sector/modules/domain',
                          'ssh': 'ssh://git@gitlab:2222/global-sector/local-sector/com/sector/modules/domain/com-module.git',
                          'url': 'https://gitlab/global-sector/local-sector/com/sector/modules/domain/com-module',
                          'name': 'com-module'}
        component_project = {'id': 34292,
                             'archived': False,
                             'namespace': 'global-sector/local-sector/com/sector/components',
                             'ssh': 'ssh://git@gitlab:2222/global-sector/local-sector/com/sector/components/com-component.git',
                             'url': 'https://gitlab/global-sector/local-sector/com/sector/components/com-component',
                             'name': 'com-component'}
        self.assertEqual(projects, [module_project, component_project])


if __name__ == '__main__':
    unittest.main()
