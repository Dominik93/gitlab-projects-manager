import { Injectable } from '@angular/core';
import { Subject } from 'rxjs';
import { emptyError, ErrorStatusData } from './error-status';


@Injectable({
  providedIn: 'root'
})
export class ErrorStatusService {

  private errorSubject: Subject<ErrorStatusData> = new Subject<ErrorStatusData>();

  constructor() { }

  setError(error: ErrorStatusData) {
    this.errorSubject.next(error);
  }

  clear() {
    this.errorSubject.next(emptyError());
  }

  getError() {
    return this.errorSubject.asObservable();
  }
}
