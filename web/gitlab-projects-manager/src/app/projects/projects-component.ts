import { Component, inject, OnInit } from '@angular/core';
import { ProjectsService } from './projects-service';
import { FormsModule } from '@angular/forms';
import { AddNamespace } from "../add-namespace/add-namespace";
import { Search } from "../search/search";
import { ProgressBar } from "../progress-bar/progress-bar";
import { ProgressBarService } from '../progress-bar/progress-bar-service';
import { ErrorStatus } from "../error-status/error-status";
import { ErrorStatusService } from '../error-status/error-status-service';
import { NamespaceService } from '../add-namespace/namespace-service';
import { GitActionsService } from '../git/git-actions-service';
import { BumpDependencyInput, Maven } from "../maven/maven";
import { MavenService } from '../maven/maven-service';
import { SearchResults } from '../search/search-results';

type Project = {
  id: string,
  characteristics: Characteristic[]
}

type Characteristic = {
  name: string,
  value: any
}

@Component({
  selector: 'app-projects-component',
  imports: [FormsModule, AddNamespace, Search, SearchResults, ProgressBar, ErrorStatus, Maven],
  templateUrl: './projects-component.html',
  styleUrl: './projects-component.css'
})
export class ProjectsComponent implements OnInit {

  projectsService: ProjectsService = inject(ProjectsService);

  namespaceService: NamespaceService = inject(NamespaceService);

  gitActionsService: GitActionsService = inject(GitActionsService);

  mavenService: MavenService = inject(MavenService);

  progressBarService: ProgressBarService = inject(ProgressBarService);

  errorStatusService: ErrorStatusService = inject(ErrorStatusService);

  headers: string[] = [];

  namespaces: string[] = [];
  
  selectedNamespace = "";

  projects: Project[] = [];

  projectId?: string;

  filteredProjects: Project[] = [];

  filteredProjectsIds: string[] = []

  containsSearchResults = false;

  filters: { [id: string]: any } = {};

  loading = false;

  ngOnInit(): void {
    this.fetchNamespaces();
    this.progressBarService.loading().subscribe(isLoading => {
      this.loading = isLoading;
    })
    this.namespaceService.addedEvent().subscribe(() => {
      this.fetchNamespaces();
    })
  }

  onFilterChange(filter: string, $event: any) {
    this.filters[filter] = $event.target.value
    this.filteredProjects = this.projects
    for (let key in this.filters) {
      let value = this.filters[key];
      this.filteredProjects = this.filteredProjects
        .filter(p => p.characteristics.filter(c => c.name == key).some(c => value === '' || this.filter(c, value)));
      this.filteredProjectsIds = this.filteredProjects.map(p => p.id);
    }
  }

  onSelectNamespace(name: string) {
    this.selectedNamespace = name;
    this.fetchProjects();
  }

  onLoad() {
    this.progressBarService.startLoading();
    this.namespaceService.load(this.selectedNamespace).subscribe(this.action(() => this.fetchProjects()));
  }

  onDelete() {
    this.progressBarService.startLoading();
    this.namespaceService.delete(this.selectedNamespace).subscribe(this.action(() => {
      this.selectedNamespace = ""
      this.projects = []
      this.filteredProjects = []
      this.filteredProjectsIds = []
      this.headers = []
      this.fetchNamespaces();
    }));
  }

  onClone() {
    const projectIds = this.projectId ? [this.projectId] : this.filteredProjectsIds;
    this.projectId = undefined;
    this.progressBarService.startLoading();
    this.gitActionsService.clone(this.selectedNamespace, projectIds).subscribe(this.action(() => { this.fetchProjects() }));
  }

  onPull() {
    const projectIds = this.projectId ? [this.projectId] : this.filteredProjectsIds;
    this.projectId = undefined;
    this.progressBarService.startLoading();
    this.gitActionsService.pull(this.selectedNamespace, projectIds).subscribe(this.action(() => this.fetchProjects()));
  }

  onStatus() {
    const projectIds = this.projectId ? [this.projectId] : this.filteredProjectsIds;
    this.projectId = undefined;
    this.progressBarService.startLoading();
    this.gitActionsService.status(this.selectedNamespace, projectIds).subscribe(this.action(() => this.fetchProjects()));
  }

  onBumpDependency(input: BumpDependencyInput) {
    const projectIds = this.projectId ? [this.projectId] : this.filteredProjectsIds;
    this.projectId = undefined;
    this.mavenService.bumpDependency(this.selectedNamespace, projectIds, input)
  }

  onContainsResults($event: boolean) {
    this.containsSearchResults = $event;
  }

  private fetchNamespaces() {
    this.progressBarService.startLoading();
    this.projectsService.getNamespaces().subscribe(this.action((res: any) => this.namespaces = res));
  }

  private fetchProjects() {
    if (this.selectedNamespace === '') {
      return;
    }
    this.progressBarService.startLoading();
    this.projectsService.getProjects(this.selectedNamespace)
      .subscribe(res => {
        this.projects = [];
        this.filteredProjects = [];
        this.filteredProjectsIds = [];
        res.forEach(item => {
          const characteristics: Characteristic[] = [];
          for (const key in item) {
            if (!this.headers.includes(key)) {
              this.headers.push(key);
            }
            characteristics.push({ name: key, value: item[key] });
          }
          this.projects.push({ id: item['id'], characteristics: characteristics });
          this.filteredProjects.push({ id: item['id'], characteristics: characteristics });
          this.filteredProjectsIds.push(item['id']);
        });
        this.progressBarService.stopLoading();
      });
  }

  private filter(characteristic: Characteristic, value: any): boolean {
    return String(characteristic.value).includes(value);
  }

  private action(nextCallback?: Function) {
    return {
      next: (res: any) => {
        this.progressBarService.stopLoading();
        this.errorStatusService.clear();
        if (nextCallback) {
          nextCallback(res);
        }
      }, error: (res: any) => {
        this.progressBarService.stopLoading();
        this.errorStatusService.setError({ occured: true, httpMessage: res.message, message: res.error.message });
      }
    };
  }

}
