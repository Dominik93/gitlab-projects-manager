import { Component, inject, Input } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { ErrorStatusService } from '../error-status/error-status-service';
import { ProgressBarService } from '../progress-bar/progress-bar-service';
import { SearchService } from './search-service';
import { NamespaceService } from '../namespace/namespace-service';
import { ProjectsService } from '../projects/projects-service';

export type SearchInput = {
  name?: string,
  text?: string,
  textRegexp?: boolean,
  file?: string,
  fileRegexp?: boolean,
  showContent?: boolean,
}

@Component({
  selector: 'app-search',
  imports: [FormsModule],
  templateUrl: './search.html',
  styleUrl: './search.css'
})
export class Search {
  searchService: SearchService = inject(SearchService);

  namespaceService: NamespaceService = inject(NamespaceService);

  projectsService: ProjectsService = inject(ProjectsService);

  progressBarService: ProgressBarService = inject(ProgressBarService);

  errorStatusService: ErrorStatusService = inject(ErrorStatusService);

  @Input()
  name: string = ""
  
  namespace: string = ""

  projects: string[] = []

  searchInput: SearchInput = {};

  ngOnInit(): void {
    this.namespaceService.selectedNamespace().subscribe(namespace => {
      this.namespace = namespace;
    })
    this.projectsService.selectedProjects().subscribe(projects => {
      this.projects = projects;
    })
  }

  onSearch() {
    this.progressBarService.start()
    this.searchService.search(this.namespace, this.searchInput, this.projects).subscribe({
      next: (res) => {
        this.progressBarService.stop()
        this.errorStatusService.clear();
        this.searchService.newResult(res)
      },
      error: (errorResponse: any) => {
        this.progressBarService.stop()
        this.errorStatusService.set({ httpMessage: errorResponse.message, message: errorResponse.error.message });
      }
    });
  }
}
