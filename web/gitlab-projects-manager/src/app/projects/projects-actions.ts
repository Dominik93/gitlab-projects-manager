import { Component, inject } from '@angular/core';
import { ErrorStatusService } from '../error-status/error-status-service';
import { GitActionsService } from '../git/git-actions-service';
import { Maven } from '../maven/maven';
import { NamespaceService } from '../namespace/namespace-service';
import { ProgressBarService } from '../progress-bar/progress-bar-service';
import { ProjectsService } from './projects-service';
import { Search } from "../search/search";
import { SearchResults } from "../search/search-results";

@Component({
  selector: 'app-projects-actions',
  imports: [Search, Maven, SearchResults],
  templateUrl: './projects-actions.html',
  styleUrl: './projects-actions.css'
})
export class ProjectsActions {

  projectsService: ProjectsService = inject(ProjectsService);

  namespaceService: NamespaceService = inject(NamespaceService);

  gitActionsService: GitActionsService = inject(GitActionsService);

  progressBarService: ProgressBarService = inject(ProgressBarService);

  errorStatusService: ErrorStatusService = inject(ErrorStatusService);

  selectedNamespace = "";

  projects: string[] = [];

  loading = false;

  ngOnInit(): void {
    this.progressBarService.loading().subscribe(isLoading => this.loading = isLoading);
    this.namespaceService.selectedNamespace().subscribe(namespace => this.selectedNamespace = namespace);
    this.projectsService.selectedProjects().subscribe(projects => this.projects = projects);
  }
  
  onLoad() {
    this.progressBarService.start();
    this.namespaceService.load(this.selectedNamespace).subscribe(this.action(() => this.projectsService.reload()));
  }

  onClone() {
    this.progressBarService.start();
    this.gitActionsService.clone(this.selectedNamespace, this.projects).subscribe(this.action(() => this.projectsService.reload()));
  }

  onPull() {
    this.progressBarService.start();
    this.gitActionsService.pull(this.selectedNamespace, this.projects).subscribe(this.action(() => this.projectsService.reload()));
  }

  onStatus() {
    this.progressBarService.start();
    this.gitActionsService.status(this.selectedNamespace, this.projects).subscribe(this.action(() => this.projectsService.reload()));
  }

  private action(nextCallback?: Function) {
    return {
      next: (res: any) => {
        this.progressBarService.stop();
        this.errorStatusService.clear();
        if (nextCallback) {
          nextCallback(res);
        }
      },
      error: (errorResponse: any) => {
        this.progressBarService.stop();
        this.errorStatusService.set({ httpMessage: errorResponse.message, message: errorResponse.error.message });
      }
    };
  }
}
