import { Component, inject, Input } from '@angular/core';
import { SearchService } from './search-service';
import { ProgressBarService } from '../progress-bar/progress-bar-service';
import { ErrorStatusService } from '../error-status/error-status-service';
import { NamespaceService } from '../namespace/namespace-service';

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

  namespaceService: NamespaceService = inject(NamespaceService);

  progressBarService: ProgressBarService = inject(ProgressBarService);

  errorStatusService: ErrorStatusService = inject(ErrorStatusService);

  @Input()
  name: string = ""

  namespace: string = ""

  searchResult?: SearchResult;

  searchResults: string[] = [];

  ngOnInit(): void {
    this.namespaceService.selectedNamespace().subscribe(namespace => {
      this.namespace = namespace;
      this.fetchSearchResults();
    });
    this.searchService.getNewResult().subscribe(() => this.fetchSearchResults())
  }

  onSearchResult(result: string) {
    this.progressBarService.start()
    this.searchService.getSearchResult(this.namespace, result).subscribe({
      next: (searchResult) => {
        this.progressBarService.stop()
        this.errorStatusService.clear();
        this.searchResult = searchResult;
      },
      error: (errorResponse: any) => {
        this.progressBarService.stop()
        this.errorStatusService.set({ httpMessage: errorResponse.message, message: errorResponse.error.message });
      }
    });
  }

  private fetchSearchResults() {
    this.progressBarService.start()
    this.searchService.getSearchResults(this.namespace).subscribe({
      next: (searchResults) => {
        this.progressBarService.stop()
        this.errorStatusService.clear();
        this.searchResults = searchResults;
      },
      error: (errorResponse: any) => {
        this.progressBarService.stop()
        this.errorStatusService.set({ httpMessage: errorResponse.message, message: errorResponse.error.message });
      }
    });
  }

}
