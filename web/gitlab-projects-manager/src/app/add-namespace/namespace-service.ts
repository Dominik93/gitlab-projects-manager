import { Injectable } from '@angular/core';
import { Observable, Subject } from 'rxjs';
import { AddNamespaceInput } from './add-namespace';
import { HttpClient } from '@angular/common/http';


@Injectable({
  providedIn: 'root'
})
export class NamespaceService {

  private _namespaceAdded: Subject<boolean> = new Subject<boolean>();

  private readonly api = "http://localhost:8000"

  constructor(private http: HttpClient) { }

  added() {
    this._namespaceAdded.next(true);
  }

  addedEvent() {
    return this._namespaceAdded.asObservable();
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

}
