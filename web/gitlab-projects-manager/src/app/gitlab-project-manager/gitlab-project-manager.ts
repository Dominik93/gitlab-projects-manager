import { Component } from '@angular/core';
import { ProjectsComponent } from "../projects/projects-component";
import { ProgressBar } from "../progress-bar/progress-bar";
import { ErrorStatus } from "../error-status/error-status";

@Component({
  selector: 'app-gitlab-project-manager',
  imports: [ProjectsComponent, ProgressBar, ErrorStatus],
  templateUrl: './gitlab-project-manager.html',
  styleUrl: './gitlab-project-manager.css'
})
export class GitlabProjectManager {

}
