import { HttpClient } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { map, Observable, Subject } from 'rxjs';
import { Service } from '../service';
import { Dependency } from '../maven/maven';


@Injectable({
  providedIn: 'root'
})
export class ProjectsService {

  http: HttpClient = inject(HttpClient);

  private _selectedProjects: Subject<string[]> = new Subject<string[]>();

  private _reload: Subject<boolean> = new Subject<boolean>();

  reload() {
    this._reload.next(true);
  }

  reloaded() {
    return this._reload.asObservable();
  }

  select(projectsIds: string[]) {
    this._selectedProjects.next(projectsIds);
  }

  selectedProjects() {
    return this._selectedProjects.asObservable();
  }

  getProjects(namespace: string): Observable<{ [id: string]: any }[]> {
    return this.http.get(`${Service.baseUrl()}/namespace/${namespace}`).pipe(map(value => value as { [id: string]: any }[]));
  }

  bumpDependency(namespace: string, dependencies: Dependency[], parent: string, version: string, message: string, ids?: string[]): Observable<any> {
    const request = {
      "projectsIds": ids,
      "release_notes": { "version": version, "message": message },
      "dependencies": dependencies,
      "parent": parent
    }
    return this.http.patch(`${Service.baseUrl()}/namespace/${namespace}/bump-dependencies`, request);
  }

}
