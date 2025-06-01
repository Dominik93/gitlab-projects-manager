import { Component, inject, OnInit } from '@angular/core';
import { ProjectsService } from './projects-service';
import { FormsModule } from '@angular/forms';

export type SearchInput = {
  text?: string,
  textRegexp?: boolean,
  file?: string,
  fileRegexp?: boolean,
  showContent?: boolean,
}

export type SearchHit = {
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

  headers: string[] = []

  projects: Project[] = []

  filteredProjects: Project[] = []

  groupId = "";

  searchInput: SearchInput = {}
  
  searchResult: SearchHit[] = []

  filters: { [id: string]: any } = {}

  loading = false;

  error = false;

  ngOnInit(): void {
    this.fetchProjects();
  }

  onFilterChange(filter: string, $event: any) {
    this.filters[filter] = $event.target.value
    this.filteredProjects = this.projects
    for (let key in this.filters) {
      let value = this.filters[key];
      this.filteredProjects = this.filteredProjects
        .filter(p => p.characteristics.filter(c => c.name == key)
          .some(c => value === '' || c.value.includes(value)));
    }
  }

  onLoad() {
    this.loading = true;
    this.projectsService.load(this.groupId).subscribe(this.action());
    this.fetchProjects();
  }

  onReload() {
    this.loading = true;
    this.projectsService.reload(this.groupId).subscribe(this.action());
    this.fetchProjects();
  }

  onCloneAll() {
    this.loading = true;
    this.projectsService.clone(this.groupId, this.filteredProjects.map(p => p.id)).subscribe(this.action());
    this.fetchProjects();
  }

  onClone(id: string) {
    this.loading = true;
    this.projectsService.clone(this.groupId, [id]).subscribe(this.action());
    this.fetchProjects();
  }

  onPull(id: string) {
    this.loading = true;
    this.projectsService.pull(this.groupId, [id]).subscribe(this.action());
    this.fetchProjects();
  }

  onPullAll() {
    this.loading = true;
    this.projectsService.pull(this.groupId, this.filteredProjects.map(p => p.id)).subscribe(this.action());
    this.fetchProjects();
  }

  onStatus(id: string) {
    this.loading = true;
    this.projectsService.status(this.groupId, [id]).subscribe(this.action());
    this.fetchProjects();
  }

  onStatusAll() {
    this.loading = true;
    this.projectsService.status(this.groupId, this.filteredProjects.map(p => p.id)).subscribe(this.action());
    this.fetchProjects();
  }

  onSearch() {
    this.loading = true;
    this.projectsService.search(this.groupId, this.searchInput, this.filteredProjects.map(p => p.id))
      .subscribe(this.action((res: any) => {this.searchResult = res}));
  }

  private action(nextCallback?: Function) {
    return {
      next: (res: any) => {
        this.loading = false;
        this.error = false;
        console.log('res', res, this.loading, this.error)
        if (nextCallback) {
          console.log('trycollback', res)
          nextCallback(res);
        }
      }, error: () => {
        this.loading = false;
        this.error = true;
      }
    };
  }

  private fetchProjects() {
    if (this.groupId === '') {
      return
    }
    this.loading = true;
    this.projectsService.getProjects(this.groupId)
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
          this.loading = false;
        });
      });
  }


}
