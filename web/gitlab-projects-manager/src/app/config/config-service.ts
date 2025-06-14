import { HttpClient } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { map, Observable } from 'rxjs';
import { Service } from '../service';


@Injectable({
  providedIn: 'root'
})
export class ConfigService {

  http: HttpClient = inject(HttpClient);

  getConfig(): Observable<string> {
    return this.http.get(`${Service.baseUrl()}/config`).pipe(map(value => JSON.stringify(value, null, 2)));
  }

  saveConfig(content: string): Observable<any> {
    return this.http.post(`${Service.baseUrl()}/config`, content);
  }

}
