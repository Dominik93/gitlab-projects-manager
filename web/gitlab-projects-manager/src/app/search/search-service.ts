import { HttpClient } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { map, Observable, Subject } from 'rxjs';
import { SearchInput } from '../search/search';
import { SearchHit, SearchResult } from './search-results';
import { Service } from '../service';


@Injectable({
  providedIn: 'root'
})
export class SearchService {

  http: HttpClient = inject(HttpClient);

  private result: Subject<SearchHit[]> = new Subject<SearchHit[]>();

  newResult(result: SearchHit[]) {
    this.result.next(result);
  }

  getNewResult() {
    return this.result.asObservable();
  }
  
  getSearchResults(namespace: string): Observable<string[]> {
    return this.http.get(`${Service.baseUrl()}/namespace/${namespace}/search`).pipe(map(value => value as string[]));
  }

  getSearchResult(namespace: string, result: string): Observable<SearchResult> {
    return this.http.get(`${Service.baseUrl()}/namespace/${namespace}/search/${result}`).pipe(map(value => value as SearchResult));
  }

  search(namespace: string, input: SearchInput, ids?: string[]): Observable<SearchHit[]> {
    const request = {
      "name": input.name,
      "projectsIds": ids,
      "searchText": input.text,
      "searchRegex": input.textRegexp,
      "fileText": input.file,
      "fileRegex": input.fileRegexp,
      "showContent": input.showContent
    }
    return this.http.post(`${Service.baseUrl()}/namespace/${namespace}/search`, request)
      .pipe(map(value => value as SearchHit[]));
  }

}