import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { map, Observable } from 'rxjs';
import { SearchHit, SearchInput } from './projects-component';


@Injectable({
  providedIn: 'root'
})
export class ProjectsService {

  private readonly api = "http://localhost:8000"

  constructor(private http: HttpClient) { }

  load(groupId: string): Observable<any> {
    return this.http.post(`${this.api}/namespace/${groupId}`, {});
  }

  reload(groupId: string): Observable<any> {
    return this.http.patch(`${this.api}/namespace/${groupId}`, {});
  }

  getProjects(groupId: string): Observable<{ [id: string]: any }[]> {
    return this.http.get(`${this.api}/namespace/${groupId}/projects`).pipe(map(value => value as { [id: string]: any }[]));
  }

  clone(groupId: string, ids?: string[]): Observable<any> {
    const request = { "projects_ids": ids }
    return this.http.post(`${this.api}/namespace/${groupId}/projects/clone`, request);
  }

  pull(groupId: string, ids?: string[]): Observable<any> {
    const request = { "projects_ids": ids }
    return this.http.post(`${this.api}/namespace/${groupId}/projects/pull`, request);
  }

  status(groupId: string, ids?: string[]): Observable<any> {
    const request = { "projects_ids": ids }
    return this.http.post(`${this.api}/namespace/${groupId}/projects/status`, request);
  }

  search(groupId: string, input: SearchInput, ids?: string[]): Observable<SearchHit[]> {
    const request = {
      "projects_ids": ids,
      "search_text": !input.textRegexp ? input.text : undefined,
      "search_regex": input.textRegexp ? input.text : undefined,
      "file_text": !input.fileRegexp ? input.file : undefined,
      "file_regex": input.fileRegexp ? input.file : undefined,
      "show_content": input.showContent
    }
    return this.http.post(`${this.api}/namespace/${groupId}/projects/search`, request)
      .pipe(map(value => value as SearchHit[]));
  }

}
