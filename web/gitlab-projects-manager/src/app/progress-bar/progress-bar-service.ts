import { Injectable } from '@angular/core';
import { Subject } from 'rxjs';



@Injectable({
  providedIn: 'root'
})
export class ProgressBarService {

  private loadingSubject: Subject<boolean> = new Subject<boolean>();

  constructor() { }
  
  startLoading() {
    this.loadingSubject.next(true);
  }

  stopLoading() {
    this.loadingSubject.next(false);
  }
  
  loading() {
    return this.loadingSubject.asObservable();
  }
}
