import { Injectable } from '@angular/core';
import { Subject } from 'rxjs';
import { SearchHit } from './search-results';


@Injectable({
  providedIn: 'root'
})
export class SearchResultService {

  private result: Subject<SearchHit[]> = new Subject<SearchHit[]>();

  constructor() { }

  newResult(result: SearchHit[]) {
    this.result.next(result);
  }

  getNewResult() {
    return this.result.asObservable();
  }

}
