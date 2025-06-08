import { inject, Injectable } from '@angular/core';
import { BumpDependencyInput } from './maven';
import { ErrorStatusService } from '../error-status/error-status-service';
import { GitActionsService } from '../git/git-actions-service';
import { ProgressBarService } from '../progress-bar/progress-bar-service';
import { ProjectsService } from '../projects/projects-service';


@Injectable({
  providedIn: 'root'
})
export class MavenService {
  projectsService: ProjectsService = inject(ProjectsService);

  progressBarService: ProgressBarService = inject(ProgressBarService);

  errorStatusService: ErrorStatusService = inject(ErrorStatusService);

  gitActionsService: GitActionsService = inject(GitActionsService);

  bumpDependency(namespace: string, projectIds: string[], bumpDependencyInput: BumpDependencyInput) {
    const branch = bumpDependencyInput.branch;
    const dependency = bumpDependencyInput.dependency;
    const version = bumpDependencyInput.version;
    const message = bumpDependencyInput.message;
    const ids = projectIds;
    if (!branch || !dependency || !version || !message || !ids) {
      return
    }
    this.progressBarService.startLoading();
    this.gitActionsService.createBranch(namespace, branch, ids).subscribe({
      next: () => {
        this.projectsService.bumpDependency(namespace, dependency, version, ids).subscribe({
          next: () => {
            this.gitActionsService.commit(namespace, message, ids).subscribe({
              next: () => {
                this.gitActionsService.push(namespace, ids).subscribe({
                  next: () => {
                    this.progressBarService.stopLoading()
                    this.errorStatusService.clear();
                  },
                  error: (res) => {
                    this.progressBarService.stopLoading()
                    this.errorStatusService.setError({ occured: true, httpMessage: res.message, message: res.error.message });
                  }
                })
              },
              error: (res) => {
                this.progressBarService.stopLoading()
                this.errorStatusService.setError({ occured: true, httpMessage: res.message, message: res.error.message });
              }
            })
          },
          error: (res) => {
            this.progressBarService.stopLoading()
            this.errorStatusService.setError({ occured: true, httpMessage: res.message, message: res.error.message });
          }
        })
      },
      error: (res) => {
        this.progressBarService.stopLoading()
        this.errorStatusService.setError({ occured: true, httpMessage: res.message, message: res.error.message });
      }
    });
  }
}
