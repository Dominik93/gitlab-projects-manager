import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { map, Observable } from 'rxjs';
import { SearchInput } from '../search/search';
import { SearchHit, SearchResult } from './search-results';


@Injectable({
  providedIn: 'root'
})
export class SearchService {

  private readonly api = "http://localhost:8000"

  constructor(private http: HttpClient) { }


  getSearchResults(namespace: string): Observable<string[]> {
    return this.http.get(`${this.api}/namespace/${namespace}/search`).pipe(map(value => value as string[]));
  }

  getSearchResult(namespace: string, result: string): Observable<SearchResult> {
    return this.http.get(`${this.api}/namespace/${namespace}/search/${result}`).pipe(map(value => value as SearchResult));
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
    return this.http.post(`${this.api}/namespace/${namespace}/search`, request)
      .pipe(map(value => value as SearchHit[]));
  }

}