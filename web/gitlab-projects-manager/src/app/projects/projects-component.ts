import { Component, inject, OnInit } from '@angular/core';
import { ProjectsService } from './projects-service';
import { FormsModule } from '@angular/forms';
import { ProgressBarService } from '../progress-bar/progress-bar-service';
import { ErrorStatusService } from '../error-status/error-status-service';
import { NamespaceService } from '../namespace/namespace-service';
import { Namespace } from "../namespace/namespace";
import { VisiblePipe } from "./visible-pipe";
import { ProjectsActions } from "./projects-actions";

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
  imports: [FormsModule, Namespace, VisiblePipe, ProjectsActions],
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
      let visible = false;
      for (let key in this.filters) {
        const value = this.filters[key];
        const characteristic = p.characteristics.find(c => c.name === key);
        if (characteristic) {
          visible = visible || (value === '' || String(characteristic.value).includes(value));
        }
      }
      p.visible = visible;
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
    this.projectsService.getProjects(this.selectedNamespace)
      .subscribe(projects => {
        this.projects = [];
        projects.forEach(item => {
          const characteristics: Characteristic[] = [];
          for (const key in item) {
            if (!this.headers.includes(key)) {
              this.headers.push(key);
            }
            characteristics.push({ name: key, value: item[key] });
          }
          this.projects.push({ id: item['id'], characteristics: characteristics, selected: false, visible: true });
        });
        this.progressBarService.stop();
      });
  }

}
