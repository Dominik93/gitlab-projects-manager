import { inject, Injectable } from '@angular/core';
import { BumpDependencyInput, CommitInfo, Dependency, ReleaseNotes } from './maven';
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
    const commitInfo = bumpDependencyInput.commit;
    const dependencies = bumpDependencyInput.dependencies;
    const releaseNotes = bumpDependencyInput.releaseNotes;
    const parent = bumpDependencyInput.parent;
    const ids = projectIds;
    if (!commitInfo || !dependencies || !releaseNotes || !ids) {
      return
    }
    this.progressBarService.start();
    this.gitActionsService.createBranch(namespace, commitInfo.branch, ids).subscribe({
      next: () => {
        this.bumpDependencies(namespace, commitInfo, releaseNotes, dependencies, parent, ids);
      },
      error: (errorResponse) => this.error(errorResponse)
    });
  }

  private bumpDependencies(namespace: string, commitInfo: CommitInfo, releaseNotes: ReleaseNotes, dependencies: Dependency[], parent: string, ids: string[]) {
    this.projectsService.bumpDependency(namespace, dependencies, parent, releaseNotes.version, releaseNotes.message, ids).subscribe({
      next: () => {
        this.gitActionsService.commit(namespace, commitInfo.message, ids).subscribe({
          next: () => {
            this.gitActionsService.push(namespace, ids).subscribe({
              next: () => {
                this.gitActionsService.createMergeRquest(namespace, commitInfo.message, commitInfo.branch, ids).subscribe({
                  next: () => {
                    this.progressBarService.stop();
                    this.errorStatusService.clear();
                  },
                  error: (errorResponse) => this.error(errorResponse)
                })
              },
              error: (errorResponse) => this.error(errorResponse)
            })
          },
          error: (errorResponse) => this.error(errorResponse)
        })
      },
      error: (errorResponse) => this.error(errorResponse)
    })
  }

  private error(errorResponse: any) {
    this.progressBarService.stop();
    this.errorStatusService.set({ httpMessage: errorResponse.message, message: errorResponse.error.message });
  }
}
