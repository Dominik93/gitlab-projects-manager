import { Component, EventEmitter, inject, Input, Output } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { ErrorStatusService } from '../error-status/error-status-service';
import { ProgressBarService } from '../progress-bar/progress-bar-service';
import { SearchResultService } from './search-result-service';
import { SearchService } from './search-service';

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

  searchResultService: SearchResultService = inject(SearchResultService);

  progressBarService: ProgressBarService = inject(ProgressBarService);

  errorStatusService: ErrorStatusService = inject(ErrorStatusService);

  @Input()
  name: string = ""

  @Input()
  namespace: string = ""

  @Input()
  projects: string[] = []

  @Output()
  search = new EventEmitter<SearchInput>();

  searchInput: SearchInput = {};

  onSearch() {
    this.progressBarService.startLoading()
    this.searchService.search(this.namespace, this.searchInput, this.projects).subscribe({
      next: (res) => {
        this.progressBarService.stopLoading()
        this.errorStatusService.clear();
        this.searchResultService.newResult(res)
      },
      error: (res: any) => {
        this.progressBarService.stopLoading()
        this.errorStatusService.setError({ occured: true, httpMessage: res.message, message: res.error.message });
      }
    });
  }
}
