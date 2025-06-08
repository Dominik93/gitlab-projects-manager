import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { map, Observable } from 'rxjs';


@Injectable({
  providedIn: 'root'
})
export class ProjectsService {

  private readonly api = "http://localhost:8000"

  constructor(private http: HttpClient) { }

  getNamespaces(): Observable<string[]> {
    return this.http.get(`${this.api}/namespace`).pipe(map(value => value as string[]));
  }

  getProjects(namespace: string): Observable<{ [id: string]: any }[]> {
    return this.http.get(`${this.api}/namespace/${namespace}`).pipe(map(value => value as { [id: string]: any }[]));
  }

  bumpDependency(namespace: string, dependency: string, version: string, ids?: string[]): Observable<any> {
    const request = { "projectsIds": ids, "dependency": dependency, "version": version }
    return this.http.patch(`${this.api}/namespace/${namespace}/bump-dependency`, request);
  }

}
