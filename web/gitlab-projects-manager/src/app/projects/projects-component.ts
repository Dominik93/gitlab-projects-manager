import { Component, inject, OnInit } from '@angular/core';
import { ProjectsService } from './projects-service';
import { FormsModule } from '@angular/forms';
import { ProgressBarService } from '../progress-bar/progress-bar-service';
import { ErrorStatusService } from '../error-status/error-status-service';
import { NamespaceService } from '../namespace/namespace-service';
import { VisiblePipe } from "./visible-pipe";

export type Project = {
  id: string,
  characteristics: Characteristic[],
  visible: boolean,
  selected: boolean
}

export type Characteristic = {
  name: string,
  value: any
}

@Component({
  selector: 'app-projects-component',
  imports: [FormsModule, VisiblePipe],
  templateUrl: './projects-component.html',
  styleUrl: './projects-component.css'
})
export class ProjectsComponent implements OnInit {

  projectsService: ProjectsService = inject(ProjectsService);

  namespaceService: NamespaceService = inject(NamespaceService);

  progressBarService: ProgressBarService = inject(ProgressBarService);

  errorStatusService: ErrorStatusService = inject(ErrorStatusService);

  headers: string[] = [];

  selectedNamespace = "";

  projects: Project[] = [];

  filters: { [id: string]: any } = {};

  loading = false;

  ngOnInit(): void {
    this.progressBarService.loading().subscribe(isLoading => this.loading = isLoading);
    this.namespaceService.selectedNamespace().subscribe(namespace => {
      this.selectedNamespace = namespace;
      this.fetchProjects();
    });
    this.projectsService.reloaded().subscribe(() => this.fetchProjects());
  }

  onFilterChange(filter: string, $event: any) {
    this.filters[filter] = $event.target.value;
    this.projects.forEach(p => {
      p.visible = this.isVisible(p);
      p.selected = p.selected && p.visible;
    })
  }

  onSelectAll($event: any) {
    this.projects.forEach(p => p.selected = $event.target.checked);
    this.projectsService.select(this.projects.filter(p => p.selected).map(p => p.id));
  }

  onSelect($event: any, project: Project) {
    project.selected = $event.target.checked;
    this.projectsService.select(this.projects.filter(p => p.selected).map(p => p.id));
  }

  private fetchProjects() {
    if (this.selectedNamespace === '') {
      return;
    }
    this.progressBarService.start();
    this.projectsService.getProjects(this.selectedNamespace).subscribe({
      next: (projects) => {
        this.projects = this.createProjects(projects);
        this.headers = this.createHeaders(projects);
        this.projectsService.select(this.projects.filter(p => p.selected).map(p => p.id));
        this.progressBarService.stop();
      },
      error: (errorResponse: any) => {
        this.progressBarService.stop()
        this.errorStatusService.set({ httpMessage: errorResponse.message, message: errorResponse.error.message });
      }
    });
  }

  private createProjects(projects: { [id: string]: any }[]): Project[] {
    const previousProjects: { [id: string]: { selected: boolean, visible: boolean }; } = {};
    this.projects.forEach(p => previousProjects[p.id] = { selected: p.selected, visible: p.visible });
    return projects.map(item => {
      const id = item['id'];
      const previousProject = previousProjects[id];
      return {
        id: id,
        characteristics: this.createCharacteristics(item),
        selected: previousProject?.selected ?? true,
        visible: previousProject?.visible ?? true
      };
    });
  }

  private createCharacteristics(item: { [id: string]: any; }) {
    const characteristics: Characteristic[] = [];
    for (const key in item) {
      characteristics.push({ name: key, value: item[key] });
    }
    return characteristics;
  }

  private createHeaders(projects: { [id: string]: any }[]): string[] {
    const headers: string[] = [];
    projects.map(item => {
      for (const key in item) {
        if (!headers.includes(key)) {
          headers.push(key);
        }
      }
    });
    return headers;
  }

  private isVisible(project: Project) {
    let visible = false;
    for (let key in this.filters) {
      const value = this.filters[key];
      const characteristic = project.characteristics.find(c => c.name === key);
      if (characteristic) {
        visible = visible || (value === '' || String(characteristic.value).includes(value));
      }
    }
    return visible;
  }

}
