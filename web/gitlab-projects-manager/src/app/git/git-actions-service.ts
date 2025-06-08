import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';


@Injectable({
  providedIn: 'root'
})
export class GitActionsService {

  private readonly api = "http://localhost:8000"

  constructor(private http: HttpClient) { }

  clone(namespace: string, ids?: string[]): Observable<any> {
    const request = { "projectsIds": ids }
    return this.http.post(`${this.api}/namespace/${namespace}/clone`, request);
  }

  pull(namespace: string, ids?: string[]): Observable<any> {
    const request = { "projectsIds": ids }
    return this.http.post(`${this.api}/namespace/${namespace}/pull`, request);
  }

  push(namespace: string, ids?: string[]): Observable<any> {
    const request = { "projectsIds": ids }
    return this.http.post(`${this.api}/namespace/${namespace}/push`, request);
  }

  commit(namespace: string, message: string, ids?: string[]): Observable<any> {
    const request = { "projectsIds": ids, "message": message }
    return this.http.post(`${this.api}/namespace/${namespace}/commit`, request);
  }

  status(namespace: string, ids?: string[]): Observable<any> {
    const request = { "projectsIds": ids }
    return this.http.post(`${this.api}/namespace/${namespace}/status`, request);
  }

  createBranch(namespace: string, branch: string, ids?: string[]): Observable<any> {
    const request = { "projectsIds": ids, "branch": branch }
    return this.http.post(`${this.api}/namespace/${namespace}/branch`, request);
  }

}
