import { Component, EventEmitter, inject, Input, Output } from '@angular/core';
import { SearchService } from './search-service';
import { ProgressBarService } from '../progress-bar/progress-bar-service';
import { ErrorStatusService } from '../error-status/error-status-service';
import { SearchResultService } from '../search/search-result-service';

export type SearchResult = {
  metadata: string;
  hits: SearchHit[];
}

export type SearchHit = {
  location: string,
  identifier: string,
  content: string
}

@Component({
  selector: 'app-search-results',
  imports: [],
  templateUrl: './search-results.html',
  styleUrl: './search-results.css'
})
export class SearchResults {

  searchService: SearchService = inject(SearchService);

  progressBarService: ProgressBarService = inject(ProgressBarService);

  errorStatusService: ErrorStatusService = inject(ErrorStatusService);

  searchResultService: SearchResultService = inject(SearchResultService);

  @Input()
  name: string = ""

  @Output()
  containsResults = new EventEmitter<boolean>();

  _namespace: string = ""

  searchResult?: SearchResult;

  searchResults: string[] = [];

  @Input()
  set namespace(namespace: string) {
    if (!namespace) {
      return;
    }
    this._namespace = namespace;
    this.fetchSearchResults();
  }

  ngOnInit(): void {
    this.searchResultService.getNewResult().subscribe(() => this.fetchSearchResults())
  }

  onSearchResult(result: string) {
    this.progressBarService.startLoading()
    this.searchService.getSearchResult(this._namespace, result).subscribe({
      next: (res) => {
        this.progressBarService.stopLoading()
        this.errorStatusService.clear();
        this.searchResult = res;
      },
      error: (res: any) => {
        this.progressBarService.stopLoading()
        this.errorStatusService.setError({ occured: true, httpMessage: res.message, message: res.error.message });
      }
    });
  }

  private fetchSearchResults() {
    this.progressBarService.startLoading()
    this.searchService.getSearchResults(this._namespace).subscribe(
      {
        next: (res) => {
          this.progressBarService.stopLoading()
          this.errorStatusService.clear();
          this.searchResults = res;
          this.containsResults.emit(this.searchResults.length > 0);
        },
        error: (res: any) => {
          this.progressBarService.stopLoading()
          this.errorStatusService.setError({ occured: true, httpMessage: res.message, message: res.error.message });
        }
      }
    );
  }

}
