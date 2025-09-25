import { Component, inject, OnInit } from '@angular/core';
import { ProjectsService } from './projects-service';
import { FormsModule } from '@angular/forms';
import { ProgressBarService } from '../progress-bar/progress-bar-service';
import { ErrorStatusService } from '../error-status/error-status-service';
import { NamespaceService } from '../namespace/namespace-service';
import { VisibleFilterService } from "./visible-filter-service";

export type Sort = {
  name: string,
  direction: 'ASC' | 'DESC'
}

export function defaultSort(): Sort {
  return { name: "", direction: "ASC" }
}

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
  imports: [FormsModule],
  templateUrl: './projects-component.html',
  styleUrl: './projects-component.css'
})
export class ProjectsComponent implements OnInit {

  projectsService: ProjectsService = inject(ProjectsService);

  namespaceService: NamespaceService = inject(NamespaceService);

  progressBarService: ProgressBarService = inject(ProgressBarService);

  errorStatusService: ErrorStatusService = inject(ErrorStatusService);

  visibleFilterService: VisibleFilterService = inject(VisibleFilterService);

  operators: { [id: string]: any; } = {
    "": (characteristicValue: any, value: any): boolean => this.contains(characteristicValue, value),
    "equals": (characteristicValue: any, value: any): boolean => this.equals(characteristicValue, value),
    "exclude": (characteristicValue: any, value: any): boolean => !this.equals(characteristicValue, value),
    "not equals": (characteristicValue: any, value: any): boolean => !this.equals(characteristicValue, value),
    "contains": (characteristicValue: any, value: any): boolean => this.contains(characteristicValue, value),
    "not contains": (characteristicValue: any, value: any): boolean => !this.contains(characteristicValue, value),
    "not": (characteristicValue: any, value: any): boolean => !this.contains(characteristicValue, value),
    "regex": (characteristicValue: any, value: any): boolean => this.regex(characteristicValue, value)
  }

  sort: Sort = defaultSort();

  headers: string[] = [];

  selectedNamespace = "";

  projects: Project[] = [];

  visibleProjects: Project[] = [];

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
    if ($event.target.value == '') {
      delete this.filters[filter];
    } else {
      this.filters[filter] = $event.target.value;
    }
    this.projects.forEach(p => {
      p.visible = this.isVisible(p);
      p.selected = p.selected && p.visible;
    })
    this.projectsService.select(this.projects.filter(p => p.selected).map(p => p.id));
    this.setVisibleProjects();
  }

  onSelectAll($event: any) {
    this.projects.forEach(p => p.selected = false);
    this.projects.filter(p => p.visible).forEach(p => p.selected = $event.target.checked);
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
        this.setVisibleProjects();
        this.sort = defaultSort();
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
    if (Object.keys(this.filters).length == 0) {
      return true;
    }
    const visibility = []
    for (let key in this.filters) {
      const value = this.filters[key];
      const operator = value.substring(0, value.indexOf(':'));
      const text = value.substring(value.indexOf(':') + 1);
      const characteristic = project.characteristics.find(c => c.name === key);
      if (characteristic) {
        const filterMethod = this.operators[operator];
        visibility.push((filterMethod === undefined ? this.operators[''] : filterMethod)(characteristic.value, text));
      }
    }
    return visibility.every(v => v);
  }

  onHeaderClick(header: string) {
    if (this.sort.name === header) {
      this.sort.direction = this.sort.direction === 'ASC' ? 'DESC' : 'ASC';
    } else {
      this.sort.name = header;
      this.sort.direction = 'ASC';
    }
    this.visibleProjects = this.visibleProjects.sort((p1, p2) => {
      const v1 = p1.characteristics.find(c => c.name === this.sort.name)?.value || '';
      const v2 = p2.characteristics.find(c => c.name === this.sort.name)?.value || '';
      if (v1 > v2) {
        return this.sort.direction === 'ASC' ? 1 : -1;
      }
      if (v1 < v2) {
        return this.sort.direction === 'ASC' ? -1 : 1;
      }
      return 0;
    });
  }

  private equals(characteristicValue: any, value: any) {
    return value === '' || String(characteristicValue) === value;
  }

  private contains(characteristicValue: any, value: any) {
    return value === '' || String(characteristicValue).includes(value);
  }

  private regex(characteristicValue: any, value: any) {
    const re = new RegExp(value);
    return value === '' || re.test(characteristicValue);
  }

  private setVisibleProjects() {
    this.visibleProjects = this.visibleFilterService.filter(this.projects);
  }

}
