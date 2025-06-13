import { HttpClient } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { Service } from '../service';


@Injectable({
  providedIn: 'root'
})
export class GitActionsService {

  http: HttpClient = inject(HttpClient);

  clone(namespace: string, ids?: string[]): Observable<any> {
    const request = { "projectsIds": ids }
    return this.http.post(`${Service.baseUrl()}/namespace/${namespace}/clone`, request);
  }

  pull(namespace: string, ids?: string[]): Observable<any> {
    const request = { "projectsIds": ids }
    return this.http.post(`${Service.baseUrl()}/namespace/${namespace}/pull`, request);
  }

  push(namespace: string, ids?: string[]): Observable<any> {
    const request = { "projectsIds": ids }
    return this.http.post(`${Service.baseUrl()}/namespace/${namespace}/push`, request);
  }

  commit(namespace: string, message: string, ids?: string[]): Observable<any> {
    const request = { "projectsIds": ids, "message": message }
    return this.http.post(`${Service.baseUrl()}/namespace/${namespace}/commit`, request);
  }

  status(namespace: string, ids?: string[]): Observable<any> {
    const request = { "projectsIds": ids }
    return this.http.post(`${Service.baseUrl()}/namespace/${namespace}/status`, request);
  }

  createBranch(namespace: string, branch: string, ids?: string[]): Observable<any> {
    const request = { "projectsIds": ids, "branch": branch }
    return this.http.post(`${Service.baseUrl()}/namespace/${namespace}/branch`, request);
  }

}
