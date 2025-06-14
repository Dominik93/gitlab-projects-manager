import { Component, inject } from '@angular/core';
import { ProjectsComponent } from "../projects/projects-component";
import { ProgressBar } from "../progress-bar/progress-bar";
import { ErrorStatus } from "../error-status/error-status";
import { Namespace } from "../namespace/namespace";
import { ProjectsActions } from "../projects/projects-actions";
import { NamespaceService } from '../namespace/namespace-service';
import { FormsModule } from '@angular/forms';
import { Config } from "../config/config";

@Component({
  selector: 'app-gitlab-project-manager',
  imports: [FormsModule, ProjectsComponent, ProgressBar, ErrorStatus, Namespace, ProjectsActions, Config],
  templateUrl: './gitlab-project-manager.html',
  styleUrl: './gitlab-project-manager.css'
})
export class GitlabProjectManager {

  namespaceService: NamespaceService = inject(NamespaceService);

  selectedNamespace = "";

  ngOnInit(): void {
    this.namespaceService.selectedNamespace().subscribe(namespace => this.selectedNamespace = namespace);
  }
}
