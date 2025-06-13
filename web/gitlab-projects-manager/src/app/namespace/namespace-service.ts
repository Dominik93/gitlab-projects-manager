import { inject, Injectable } from '@angular/core';
import { map, Observable, Subject } from 'rxjs';
import { AddNamespaceInput } from './add-namespace';
import { HttpClient } from '@angular/common/http';
import { Service } from '../service';


@Injectable({
  providedIn: 'root'
})
export class NamespaceService {

  http: HttpClient = inject(HttpClient);

  private _namespaceAdded: Subject<boolean> = new Subject<boolean>();
  
  private _selectedNamespace: Subject<string> = new Subject<string>();

  select(namespace: string) {
    this._selectedNamespace.next(namespace);
  }

  selectedNamespace() {
    return this._selectedNamespace.asObservable();
  }

  add() {
    this._namespaceAdded.next(true);
  }

  namespaceAdded() {
    return this._namespaceAdded.asObservable();
  }

  getNamespaces(): Observable<string[]> {
    return this.http.get(`${Service.baseUrl()}/namespace`).pipe(map(value => value as string[]));
  }

  addNamespace(addNamespaceInput: AddNamespaceInput) {
    const request = { "name": addNamespaceInput.name, "group": addNamespaceInput.group }
    return this.http.post(`${Service.baseUrl()}/namespace`, request);
  }

  load(namespace: string): Observable<any> {
    return this.http.get(`${Service.baseUrl()}/namespace/${namespace}`);
  }

  delete(namespace: string): Observable<any> {
    return this.http.delete(`${Service.baseUrl()}/namespace/${namespace}`);
  }

}
