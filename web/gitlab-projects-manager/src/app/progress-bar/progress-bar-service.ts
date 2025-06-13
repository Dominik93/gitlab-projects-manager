import { Injectable } from '@angular/core';
import { Subject } from 'rxjs';



@Injectable({
  providedIn: 'root'
})
export class ProgressBarService {

  private loadingSubject: Subject<boolean> = new Subject<boolean>();

  constructor() { }
  
  start() {
    this.loadingSubject.next(true);
  }

  stop() {
    this.loadingSubject.next(false);
  }
  
  loading() {
    return this.loadingSubject.asObservable();
  }
}
