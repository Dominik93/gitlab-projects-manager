import { Component, inject, OnInit } from '@angular/core';
import { ProjectsService } from './projects-service';
import { FormsModule } from '@angular/forms';

export type Namespace = {
  name: string,
  group: string,
}

export type SearchInput = {
  name?: string,
  text?: string,
  textRegexp?: boolean,
  file?: string,
  fileRegexp?: boolean,
  showContent?: boolean,
}

export type AddNamespaceInput = {
  name?: string,
  group?: string,
}

export type BumpDependencyInput = {
  ids?: string[],
  dependency?: string,
  version?: string
  message?: string,
  branch?: string,
}

export type SearchResult = {
  metadata: string;
  hits: SearchHit[];
}

export type SearchHit = {
  location: string,
  identifier: string,
  content: string
}

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
  imports: [FormsModule],
  templateUrl: './projects-component.html',
  styleUrl: './projects-component.css'
})
export class ProjectsComponent implements OnInit {



  projectsService: ProjectsService = inject(ProjectsService);

  headers: string[] = [];

  namespaces: string[] = [];

  projects: Project[] = [];

  filteredProjects: Project[] = [];

  selectedNamespace = "";

  searchInput: SearchInput = {};

  bumpDependencyInput: BumpDependencyInput = {};

  addNamespaceInput: AddNamespaceInput = {};

  searchResult?: SearchResult;

  searchResults: string[] = [];

  filters: { [id: string]: any } = {};

  loading = false;

  error = { occured: false, httpMessage: "", message: "" };

  progress: number = 0;

  interval: any;

  ngOnInit(): void {
    this.fetchNamespaces();
  }

  startLoading() {
    this.loading = true;
    this.interval = setInterval(() => {
      if (this.progress > 100) {
        this.progress = 0;
      } else {
        this.progress += 5;
      }
    }, 500)
  }

  stopLoading() {
    this.progress = 0;
    this.loading = false;
    clearInterval(this.interval);
  }

  onFilterChange(filter: string, $event: any) {
    this.filters[filter] = $event.target.value
    this.filteredProjects = this.projects
    for (let key in this.filters) {
      let value = this.filters[key];
      this.filteredProjects = this.filteredProjects
        .filter(p => p.characteristics.filter(c => c.name == key)
          .some(c => value === '' || this.filter(c, value)));
    }
  }

  onSelectNamespace(name: string) {
    this.selectedNamespace = name;
    this.fetchProjects();
    this.fetchSearchResults();
  }

  onAddNamespace() {
    this.startLoading();
    this.projectsService.addNamespace(this.addNamespaceInput).subscribe(this.action(() => this.fetchNamespaces()))
  }

  onLoad() {
    this.startLoading();
    this.projectsService.load(this.selectedNamespace).subscribe(this.action(() => this.fetchProjects()));
  }

  onDelete() {
    this.startLoading();
    this.projectsService.delete(this.selectedNamespace).subscribe(this.action(() => {
      this.selectedNamespace = ""
      this.projects = []
      this.filteredProjects = []
      this.headers = []
      this.fetchNamespaces();
    }));

  }

  onCloneAll() {
    this.startLoading();
    this.projectsService.clone(this.selectedNamespace, this.filteredProjects.map(p => p.id)).subscribe(this.action(() => this.fetchProjects()));
  }

  onClone(id: string) {
    this.startLoading();
    this.projectsService.clone(this.selectedNamespace, [id]).subscribe(this.action(() => this.fetchProjects()));
  }

  onPull(id: string) {
    this.startLoading();
    this.projectsService.pull(this.selectedNamespace, [id]).subscribe(this.action(() => this.fetchProjects()));
  }

  onPullAll() {
    this.startLoading();
    this.projectsService.pull(this.selectedNamespace, this.filteredProjects.map(p => p.id)).subscribe(this.action(() => this.fetchProjects()));
  }

  onStatus(id: string) {
    this.startLoading();
    this.projectsService.status(this.selectedNamespace, [id]).subscribe(this.action(() => this.fetchProjects()));
  }

  onStatusAll() {
    this.startLoading();
    this.projectsService.status(this.selectedNamespace, this.filteredProjects.map(p => p.id)).subscribe(this.action(() => this.fetchProjects()));
  }

  onSearch() {
    this.startLoading();
    this.projectsService.search(this.selectedNamespace, this.searchInput, this.filteredProjects.map(p => p.id))
      .subscribe(this.action(() => { this.fetchSearchResults() }));
  }

  onSearchResult(result: string) {
    this.startLoading();
    this.projectsService.getSearchResult(this.selectedNamespace, result)
      .subscribe(this.action((res: any) => { this.searchResult = res }));
  }


  onBumpDependencyAll() {
    this.bumpDependencyInput.ids = this.filteredProjects.map(p => p.id)
  }

  onBumpDependency(ids: string) {
    this.bumpDependencyInput.ids = [ids]
  }

  onVersionChanged($event: any) {
    this.bumpDependencyInput.branch = 'feature/' + this.bumpDependencyInput.dependency + '_' + $event;
    this.bumpDependencyInput.message = 'bump ' + this.bumpDependencyInput.dependency + ' ' + $event
  }

  onDependencyChanged($event: any) {
    this.bumpDependencyInput.branch = 'feature/' + $event + '_' + this.bumpDependencyInput.version;
    this.bumpDependencyInput.message = 'bump ' + $event + ' ' + this.bumpDependencyInput.version
  }

  bumpDependency() {
    const branch = this.bumpDependencyInput.branch;
    const dependency = this.bumpDependencyInput.dependency;
    const version = this.bumpDependencyInput.version;
    const message = this.bumpDependencyInput.message;
    const ids = this.bumpDependencyInput.ids
    if (!branch || !dependency || !version || !message || !ids) {
      return
    }
    this.startLoading();
    this.projectsService.createBranch(this.selectedNamespace, branch, ids).subscribe(
      this.action(() => {
        this.startLoading();
        this.projectsService.bumpDependency(this.selectedNamespace, dependency, version, ids).subscribe(
          this.action(() => {
            this.startLoading();
            this.projectsService.commit(this.selectedNamespace, message, ids).subscribe(
              this.action(() => {
                this.startLoading();
                this.projectsService.push(this.selectedNamespace, ids).subscribe(this.action())
              })
            )
          })
        )
      })
    )
  }


  private action(nextCallback?: Function) {
    return {
      next: (res: any) => {
        this.stopLoading();
        this.error = { occured: false, httpMessage: "", message: "" };
        if (nextCallback) {
          nextCallback(res);
        }
      }, error: (res: any) => {
        this.stopLoading();
        this.error = { occured: true, httpMessage: res.message, message: res.error.message };
      }
    };
  }

  private fetchNamespaces() {
    this.loading = true
    this.projectsService.getNamespaces().subscribe(this.action((res: any) => this.namespaces = res));
  }

  private fetchSearchResults() {
    this.projectsService.getSearchResults(this.selectedNamespace).subscribe(res => this.searchResults = res)
  }

  private fetchProjects() {
    if (this.selectedNamespace === '') {
      return
    }
    this.startLoading();
    this.projectsService.getProjects(this.selectedNamespace)
      .subscribe(res => {
        this.projects = [];
        this.filteredProjects = [];
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
          this.stopLoading();
        });
      });
  }

  private filter(characteristic: Characteristic, value: any): boolean {
    return String(characteristic.value).includes(value);
  }

}
