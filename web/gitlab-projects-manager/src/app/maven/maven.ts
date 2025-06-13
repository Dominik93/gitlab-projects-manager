import { Component, inject, Input } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { MavenService } from './maven-service';
import { NamespaceService } from '../namespace/namespace-service';
import { ProjectsService } from '../projects/projects-service';

export type BumpDependencyInput = {
  dependency?: string,
  version?: string,
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

  bumpDependencyInput: BumpDependencyInput = {};

  selectedNamespace = "";

  projects: string[] = [];

  ngOnInit(): void {
    this.namespaceService.selectedNamespace().subscribe(namespace => this.selectedNamespace = namespace);
    this.projectsService.selectedProjects().subscribe(projects => this.projects = projects);
  }

  onVersionChanged($event: any) {
    this.bumpDependencyInput.branch = `feature/${this.bumpDependencyInput.dependency}_${$event}`;
    this.bumpDependencyInput.message = `bump ${this.bumpDependencyInput.dependency} ${$event}`;
  }

  onDependencyChanged($event: any) {
    this.bumpDependencyInput.branch = `feature/${$event}_${this.bumpDependencyInput.version}`;
    this.bumpDependencyInput.message = `bump ${$event} ${this.bumpDependencyInput.version}`;
  }

  onBumpDependency() {
    this.mavenService.bumpDependency(this.selectedNamespace, this.projects, this.bumpDependencyInput)
  }

}
