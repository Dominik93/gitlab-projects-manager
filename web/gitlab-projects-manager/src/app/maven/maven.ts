import { Component, inject, Input } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { MavenService } from './maven-service';
import { NamespaceService } from '../namespace/namespace-service';
import { ProjectsService } from '../projects/projects-service';


export type Dependency = {
  name: string,
  version: string
}

export type BumpDependencyInput = {
  dependencies: Dependency[],
  message?: string,
  branch?: string,
}

@Component({
  selector: 'app-maven',
  imports: [FormsModule],
  templateUrl: './maven.html',
  styleUrl: './maven.css'
})
export class Maven {

  mavenService: MavenService = inject(MavenService);

  projectsService: ProjectsService = inject(ProjectsService);

  namespaceService: NamespaceService = inject(NamespaceService);

  @Input()
  name: string = ""

  bumpDependencyInput: BumpDependencyInput = { dependencies: [{ name: "", version: "" }] };

  selectedNamespace = "";

  projects: string[] = [];

  ngOnInit(): void {
    this.namespaceService.selectedNamespace().subscribe(namespace => this.selectedNamespace = namespace);
    this.projectsService.selectedProjects().subscribe(projects => this.projects = projects);
  }

  onAddNewDependency() {
    this.bumpDependencyInput.dependencies?.push({ name: "", version: "" });
  }

  onRemoveDependency() {
    this.bumpDependencyInput.dependencies?.pop();
  }

  onVersionChanged($version: any) {
    if (this.bumpDependencyInput.dependencies?.length == 1) {
      this.bumpDependencyInput.branch = `feature/${this.bumpDependencyInput.dependencies[0].name}_${$version}`;
    }
    this.bumpDependencyInput.message = `bump ${this.bumpDependencyInput.dependencies?.map(dep => dep.name + " " + dep.version).join(", ")}`;
  }

  onDependencyChanged($dependnecyName: any) {
    if (this.bumpDependencyInput.dependencies?.length == 1) {
      this.bumpDependencyInput.branch = `feature/${$dependnecyName}_${this.bumpDependencyInput.dependencies[0].version}`;
    }
    this.bumpDependencyInput.message = `bump ${this.bumpDependencyInput.dependencies?.map(dep => dep.name + " " + dep.version).join(", ")}`;
  }

  onBumpDependency() {
    this.mavenService.bumpDependency(this.selectedNamespace, this.projects, this.bumpDependencyInput)
  }

}
