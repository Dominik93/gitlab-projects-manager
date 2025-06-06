import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { map, Observable } from 'rxjs';
import { AddNamespaceInput, SearchHit, SearchInput, SearchResult } from './projects-component';


@Injectable({
  providedIn: 'root'
})
export class ProjectsService {

  private readonly api = "http://localhost:8000"

  constructor(private http: HttpClient) { }

  getNamespaces(): Observable<string[]> {
    return this.http.get(`${this.api}/namespace`).pipe(map(value => value as string[]));
  }

  getSearchResults(namespace: string): Observable<string[]> {
    return this.http.get(`${this.api}/namespace/${namespace}/search`).pipe(map(value => value as string[]));
  }

  getSearchResult(namespace: string, result: string): Observable<SearchResult> {
    return this.http.get(`${this.api}/namespace/${namespace}/search/${result}`).pipe(map(value => value as SearchResult));
  }

  addNamespace(addNamespaceInput: AddNamespaceInput) {
    const request = { "name": addNamespaceInput.name, "group": addNamespaceInput.group }
    return this.http.post(`${this.api}/namespace`, request);
  }

  load(namespace: string): Observable<any> {
    return this.http.get(`${this.api}/namespace/${namespace}`);
  }

  delete(namespace: string): Observable<any> {
    return this.http.delete(`${this.api}/namespace/${namespace}`);
  }

  getProjects(namespace: string): Observable<{ [id: string]: any }[]> {
    return this.http.get(`${this.api}/namespace/${namespace}`).pipe(map(value => value as { [id: string]: any }[]));
  }

  clone(namespace: string, ids?: string[]): Observable<any> {
    const request = { "projects_ids": ids }
    return this.http.post(`${this.api}/namespace/${namespace}/clone`, request);
  }

  pull(namespace: string, ids?: string[]): Observable<any> {
    const request = { "projects_ids": ids }
    return this.http.post(`${this.api}/namespace/${namespace}/pull`, request);
  }

  push(namespace: string, ids?: string[]): Observable<any> {
    const request = { "projects_ids": ids }
    return this.http.post(`${this.api}/namespace/${namespace}/push`, request);
  }

  commit(namespace: string, message: string, ids?: string[]): Observable<any> {
    const request = { "projects_ids": ids, "message": message }
    return this.http.post(`${this.api}/namespace/${namespace}/commit`, request);
  }

  status(namespace: string, ids?: string[]): Observable<any> {
    const request = { "projects_ids": ids }
    return this.http.post(`${this.api}/namespace/${namespace}/status`, request);
  }

  search(namespace: string, input: SearchInput, ids?: string[]): Observable<SearchHit[]> {
    const request = {
      "name": input.name,
      "projects_ids": ids,
      "search_text": input.text,
      "search_regex": input.textRegexp,
      "file_text": input.file,
      "file_regex": input.fileRegexp,
      "show_content": input.showContent
    }
    return this.http.post(`${this.api}/namespace/${namespace}/search`, request)
      .pipe(map(value => value as SearchHit[]));
  }

  createBranch(namespace: string, branch: string, ids?: string[]): Observable<any> {
    const request = { "projects_ids": ids, "branch": branch }
    return this.http.post(`${this.api}/namespace/${namespace}/branch`, request);
  }

  bumpDependency(namespace: string, dependency: string, version: string, ids?: string[]): Observable<any> {
    const request = { "projects_ids": ids, "dependency": dependency, "version": version }
    return this.http.patch(`${this.api}/namespace/${namespace}/bump-dependency`, request);
  }

}
